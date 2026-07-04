from sqlalchemy import event
from contextlib import asynccontextmanager
from time import monotonic
import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import Integer, String, create_engine, select, text
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.pool import NullPool
import libsql


load_dotenv()

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN")


def build_engine_url(database_url: str) -> str:
    if database_url.startswith("sqlite+"):
        url = database_url
    elif database_url.startswith("libsql://"):
        url = f"sqlite+{database_url}"
    elif database_url.startswith(("http://", "https://")):
        url = f"sqlite+libsql://{database_url.split('://', 1)[1]}"
    else:
        url = f"sqlite+libsql://{database_url}"

    if "secure=" not in url:
        url = f"{url}{'&' if '?' in url else '?'}secure=true"

    return url


if not TURSO_DATABASE_URL:
    raise RuntimeError("TURSO_DATABASE_URL is not set")

if not TURSO_AUTH_TOKEN:
    raise RuntimeError("TURSO_AUTH_TOKEN is not set")


engine = create_engine(
    build_engine_url(TURSO_DATABASE_URL),
    connect_args={
        "auth_token": TURSO_AUTH_TOKEN,
    },
    pool_pre_ping=True,
    # poolclass=NullPool,
    # pool_reset_on_return=None,
    # pool_size=1,
    # max_overflow=0,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
START_TIME = monotonic()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True)


class UserCreate(BaseModel):
    name: str
    username: str
    email: str


class UserRead(UserCreate):
    id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def ping_database() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok"}
    except SQLAlchemyError as exc:
        return {"status": "error", "message": str(exc)}


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="LibSQL FastAPI Demo",
              lifespan=lifespan,
              redirect_slashes=True)

conn = libsql.connect(
    database=os.environ["TURSO_DATABASE_URL"],
    auth_token=os.environ["TURSO_AUTH_TOKEN"],
)


@app.get("/ping-db")
def ping(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1")).scalar()
        return {"ok": True}
    except SQLAlchemyError as exc:
        return {"ok": False, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "uptime_seconds": round(monotonic() - START_TIME, 2),
        "db_connection": ping_database(),
    }


@app.get("/raw")
def raw():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()


@app.get("/users", response_model=list[UserRead])
def fetch_users(db: Session = Depends(get_db)):
    users = db.execute(select(User).order_by(User.id)).scalars().all()
    # db.rollback()
    return users


@app.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.model_dump())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with the same username or email already exists.",
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create the user.",
        ) from exc

    return new_user


# @event.listens_for(engine, "checkout")
# def checkout(dbapi_conn, connection_record, proxy):
#     print("CHECKOUT", id(dbapi_conn))
#
#
# @event.listens_for(engine, "checkin")
# def checkin(dbapi_conn, connection_record):
#     print("CHECKIN", id(dbapi_conn))
