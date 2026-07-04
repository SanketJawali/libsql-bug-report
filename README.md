# libsql-experimental SQLAlchemy Reproduction

This repository is a minimal reproduction project for a concurrency issue observed when using **SQLAlchemy** with **sqlalchemy-libsql** and **libsql-experimental** against a remote Turso database.

The project intentionally contains only the minimum amount of code required to reproduce the problem:

* FastAPI
* SQLAlchemy ORM
* sqlalchemy-libsql
* Remote Turso database
* A single `users` table
* One endpoint that performs a simple `SELECT`

The issue was originally discovered while load testing a larger application. This repository was created to isolate the problem and eliminate unrelated application logic.

***Check the `benchmark.md` for commands used, logs of application output, and other details of the original investigation.***

---

## Setup

### 1. Install dependencies

```bash
uv sync
```

or

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=libsql://<your-database>.turso.io
DATABASE_AUTH_TOKEN=<your-auth-token>
```

The project expects a remote Turso database containing a `users` table.

Example schema:

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    username TEXT,
    email TEXT
);
```

The reproduction was performed using 26 rows, although the exact data does not appear to matter.

---

## Running

Start the application:

```
fastapi run main.py
```

OR

```bash
uvicorn main:app --reload
```

---

## Reproducing the issue

The issue reproduces under concurrent requests using `wrk`.

Example:

```bash
wrk -t2 -c5 -d15s http://localhost:8000/users
```

The original issue was also reproduced with higher concurrency such as:

```bash
wrk -t8 -c50 -d30s http://localhost:8000/users
```

---

## Expected behavior

The endpoint should continuously return successful responses under load.

---

## Actual behavior

Under concurrent load, the application intermittently returns HTTP 500 responses.

The server logs show Rust panics originating from `libsql-experimental`, for example:

```text
thread '<unnamed>' panicked at src/lib.rs:220:65:
called `Option::unwrap()` on a `None` value
```

and

```text
thread '<unnamed>' panicked at src/lib.rs:260:42:
called `Option::unwrap()` on a `None` value
```

which propagate to Python as:

```text
pyo3_runtime.PanicException:
called `Option::unwrap()` on a `None` value
```

---

## Investigation performed

The following experiments were performed while isolating the issue:

* Reproduced using this minimal project.
* Raw libsql client (without SQLAlchemy) did **not** reproduce the panic.
* Using SQLAlchemy `NullPool` avoided the Rust panic but resulted in request timeouts due to creating a new remote connection for every request.
* Setting `pool_reset_on_return=None` did **not** eliminate the panic.
* Explicitly calling `db.rollback()` changed the failure mode, with panics occurring during cursor creation as well.

These observations suggest the issue is related to the interaction between SQLAlchemy's connection lifecycle and the `libsql-experimental` DBAPI implementation, although the exact root cause has not yet been determined.
