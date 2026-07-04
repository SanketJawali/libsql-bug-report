## Testing the application under load with `wrk`

### Testing environment:

- Fastapi server running locally with one worker initially
- DB contains 26 entries(rows). `wrk` will send GET requests to `/users` endpoint.

### Tests
1)
```
wrk -t1 -c1 -d10s http://localhost:8000/users
Running 10s test @ http://localhost:8000/users
  1 threads and 1 connections
    Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   693.64ms  137.38ms   1.13s    85.71%
    Req/Sec     0.93      0.27     1.00     92.86%
  14 requests in 10.01s, 27.84KB read
Requests/sec:      1.40
Transfer/sec:      2.78KB
```

2)
```
wrk -t1 -c1 -d10s http://localhost:8000/users
Running 10s test @ http://localhost:8000/users
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   497.58ms  176.27ms   1.02s    85.71%
    Req/Sec     1.75      0.72     3.00     60.00%
  20 requests in 10.01s, 39.77KB read
Requests/sec:      2.00
Transfer/sec:      3.97KB
```

3)
```
wrk -t1 -c1 -d10s http://localhost:8000/users
Running 10s test @ http://localhost:8000/users
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   700.51ms  154.73ms   1.23s    92.86%
    Req/Sec     0.93      0.27     1.00     92.86%
  14 requests in 10.01s, 27.84KB read
Requests/sec:      1.40
Transfer/sec:      2.78KB
```

---

4)
```
wrk -t2 -c5 -d30s http://localhost:8000/users
Running 30s test @ http://localhost:8000/users
  2 threads and 5 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.81s   218.76ms   1.98s    83.33%
    Req/Sec     0.77      1.56     5.00     87.10%
  42 requests in 30.04s, 81.71KB read
  Socket errors: connect 0, read 2, write 0, timeout 30
  Non-2xx or 3xx responses: 1
Requests/sec:      1.40
Transfer/sec:      2.72KB
```

**Errors during test:**
<details>
    ```
    INFO   127.0.0.1:35962 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35926 - "GET /users HTTP/1.1" 200

    thread '<unnamed>' panicked at src/lib.rs:260:42:
    called `Option::unwrap()` on a `None` value
        ERROR   Exception in ASGI application
    Traceback (most recent call last):
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
        result = await app(  # type: ignore[func-returns-value]
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            self.scope, self.receive, self.send
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
        return await self.app(scope, receive, send)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
        await super().__call__(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
        await self.app(scope, receive, _send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
        await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
        await self.app(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
        await route.handle(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
        await super().handle(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
        await self.app(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
        await wrap_app_handling_exceptions(app, request)(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 132, in app
        async with AsyncExitStack() as request_stack:
                ~~~~~~~~~~~~~~^^
    File "/usr/lib/python3.13/contextlib.py", line 768, in __aexit__
        raise exc
    File "/usr/lib/python3.13/contextlib.py", line 751, in __aexit__
        cb_suppress = await cb(*exc_details)
                    ^^^^^^^^^^^^^^^^^^^^^^
    File "/usr/lib/python3.13/contextlib.py", line 221, in __aexit__
        await anext(self.gen)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/concurrency.py", line 39, in contextmanager_in_threadpool
        await anyio.to_thread.run_sync(
            cm.__exit__, None, None, None, limiter=exit_limiter
        )
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
        return await get_async_backend().run_sync_in_worker_thread(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
        return await future
            ^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
        result = context.run(func, *args)
    File "/usr/lib/python3.13/contextlib.py", line 148, in __exit__
        next(self.gen)
        ~~~~^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/main.py", line 84, in get_db
        db.close()
        ~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2529, in close
        self._close_impl(invalidate=False)
        ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2598, in _close_impl
        transaction.close(invalidate)
        ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
    File "<string>", line 2, in close
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
        ret_value = fn(self, *arg, **kw)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 1422, in close
        transaction.close()
        ~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2599, in close
        self._do_close()
        ~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2737, in _do_close
        self._close_impl()
        ~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2723, in _close_impl
        self._connection_rollback_impl()
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2715, in _connection_rollback_impl
        self.connection._rollback_impl()
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1132, in _rollback_impl
        self._handle_dbapi_exception(e, None, None, None, None)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
        raise exc_info[1].with_traceback(exc_info[2])
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1130, in _rollback_impl
        self.engine.dialect.do_rollback(self.connection)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 712, in do_rollback
        dbapi_connection.rollback()
        ~~~~~~~~~~~~~~~~~~~~~~~~~^^
    pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
        INFO   127.0.0.1:35938 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35952 - "GET /users HTTP/1.1" 200

    thread '<unnamed>' panicked at src/lib.rs:260:42:
    called `Option::unwrap()` on a `None` value
        ERROR   Exception in ASGI application
    Traceback (most recent call last):
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
        result = await app(  # type: ignore[func-returns-value]
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            self.scope, self.receive, self.send
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
        return await self.app(scope, receive, send)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
        await super().__call__(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
        await self.app(scope, receive, _send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
        await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
        await self.app(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
        await route.handle(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
        await super().handle(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
        await self.app(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
        await wrap_app_handling_exceptions(app, request)(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 132, in app
        async with AsyncExitStack() as request_stack:
                ~~~~~~~~~~~~~~^^
    File "/usr/lib/python3.13/contextlib.py", line 768, in __aexit__
        raise exc
    File "/usr/lib/python3.13/contextlib.py", line 751, in __aexit__
        cb_suppress = await cb(*exc_details)
                    ^^^^^^^^^^^^^^^^^^^^^^
    File "/usr/lib/python3.13/contextlib.py", line 221, in __aexit__
        await anext(self.gen)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/concurrency.py", line 39, in contextmanager_in_threadpool
        await anyio.to_thread.run_sync(
            cm.__exit__, None, None, None, limiter=exit_limiter
        )
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
        return await get_async_backend().run_sync_in_worker_thread(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
        return await future
            ^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
        result = context.run(func, *args)
    File "/usr/lib/python3.13/contextlib.py", line 148, in __exit__
        next(self.gen)
        ~~~~^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/main.py", line 84, in get_db
        db.close()
        ~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2529, in close
        self._close_impl(invalidate=False)
        ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2598, in _close_impl
        transaction.close(invalidate)
        ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
    File "<string>", line 2, in close
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
        ret_value = fn(self, *arg, **kw)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 1422, in close
        transaction.close()
        ~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2599, in close
        self._do_close()
        ~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2737, in _do_close
        self._close_impl()
        ~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2723, in _close_impl
        self._connection_rollback_impl()
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2715, in _connection_rollback_impl
        self.connection._rollback_impl()
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1132, in _rollback_impl
        self._handle_dbapi_exception(e, None, None, None, None)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
        raise exc_info[1].with_traceback(exc_info[2])
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1130, in _rollback_impl
        self.engine.dialect.do_rollback(self.connection)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 712, in do_rollback
        dbapi_connection.rollback()
        ~~~~~~~~~~~~~~~~~~~~~~~~~^^
    pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
        INFO   127.0.0.1:35926 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35976 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35938 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35952 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35926 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35938 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35976 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35952 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35926 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35938 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35976 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35952 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35926 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35938 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35926 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35976 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35952 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35926 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35938 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35952 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35976 - "GET /users HTTP/1.1" 200

    thread '<unnamed>' panicked at src/lib.rs:220:65:
    called `Option::unwrap()` on a `None` value
        ERROR   Exception in ASGI application
    Traceback (most recent call last):
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
        result = await app(  # type: ignore[func-returns-value]
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            self.scope, self.receive, self.send
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
        return await self.app(scope, receive, send)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
        await super().__call__(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
        await self.app(scope, receive, _send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
        await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
        await self.app(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
        await route.handle(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
        await super().handle(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
        await self.app(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
        await wrap_app_handling_exceptions(app, request)(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 136, in app
        response = await f(request)
                ^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 690, in app
        raw_response = await run_endpoint_function(
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        ...<3 lines>...
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 346, in run_endpoint_function
        return await run_in_threadpool(dependant.call, **values)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/concurrency.py", line 34, in run_in_threadpool
        return await anyio.to_thread.run_sync(func)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
        return await get_async_backend().run_sync_in_worker_thread(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
        return await future
            ^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
        result = context.run(func, *args)
    File "/home/tinker/programming/libsql-demo/main.py", line 129, in fetch_users
        users = db.execute(select(User).order_by(User.id)).scalars().all()
                ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2373, in execute
        return self._execute_internal(
            ~~~~~~~~~~~~~~~~~~~~~~^
            statement,
            ^^^^^^^^^^
        ...<4 lines>...
            _add_event=_add_event,
            ^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2271, in _execute_internal
        result: Result[Any] = compile_state_cls.orm_execute_statement(
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
            self,
            ^^^^^
        ...<4 lines>...
            conn,
            ^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
        result = conn.execute(
            statement, params or {}, execution_options=execution_options
        )
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
        return meth(
            self,
            distilled_parameters,
            execution_options or NO_OPTIONS,
        )
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
        return connection._execute_clauseelement(
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
            self, distilled_params, execution_options
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
        ret = self._execute_context(
            dialect,
        ...<8 lines>...
            cache_hit=cache_hit,
        )
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1823, in _execute_context
        self._handle_dbapi_exception(
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
            e, str(statement), parameters, None, None
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
        raise exc_info[1].with_traceback(exc_info[2])
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1817, in _execute_context
        context = constructor(
            dialect, self, conn, execution_options, *args, **kw
        )
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 1438, in _init_compiled
        self.cursor = self.create_cursor()
                    ~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 1777, in create_cursor
        return self.create_default_cursor()
            ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 1783, in create_default_cursor
        return self._dbapi_connection.cursor()
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 1494, in cursor
        return self.dbapi_connection.cursor(*args, **kwargs)
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
    pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
        INFO   127.0.0.1:35938 - "GET /users HTTP/1.1" 500
        INFO   127.0.0.1:35976 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35952 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:35926 - "GET /users HTTP/1.1" 200
        INFO   127.0.0.1:43424 - "GET /users HTTP/1.1" 200

    thread '<unnamed>' panicked at src/lib.rs:260:42:
    called `Option::unwrap()` on a `None` value
        INFO   127.0.0.1:35952 - "GET /users HTTP/1.1" 200
        ERROR   Exception in ASGI application
    Traceback (most recent call last):
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
        result = await app(  # type: ignore[func-returns-value]
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            self.scope, self.receive, self.send
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
        return await self.app(scope, receive, send)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
        await super().__call__(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
        await self.app(scope, receive, _send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
        await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
        await self.app(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
        await self.middleware_stack(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
        await route.handle(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
        await super().handle(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
        await self.app(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
        await wrap_app_handling_exceptions(app, request)(scope, receive, send)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
        await app(scope, receive, sender)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 132, in app
        async with AsyncExitStack() as request_stack:
                ~~~~~~~~~~~~~~^^
    File "/usr/lib/python3.13/contextlib.py", line 768, in __aexit__
        raise exc
    File "/usr/lib/python3.13/contextlib.py", line 751, in __aexit__
        cb_suppress = await cb(*exc_details)
                    ^^^^^^^^^^^^^^^^^^^^^^
    File "/usr/lib/python3.13/contextlib.py", line 221, in __aexit__
        await anext(self.gen)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/concurrency.py", line 39, in contextmanager_in_threadpool
        await anyio.to_thread.run_sync(
            cm.__exit__, None, None, None, limiter=exit_limiter
        )
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
        return await get_async_backend().run_sync_in_worker_thread(
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )
        ^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
        return await future
            ^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
        result = context.run(func, *args)
    File "/usr/lib/python3.13/contextlib.py", line 148, in __exit__
        next(self.gen)
        ~~~~^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/main.py", line 84, in get_db
        db.close()
        ~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2529, in close
        self._close_impl(invalidate=False)
        ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2598, in _close_impl
        transaction.close(invalidate)
        ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
    File "<string>", line 2, in close
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
        ret_value = fn(self, *arg, **kw)
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 1422, in close
        transaction.close()
        ~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2599, in close
        self._do_close()
        ~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2737, in _do_close
        self._close_impl()
        ~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2723, in _close_impl
        self._connection_rollback_impl()
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2715, in _connection_rollback_impl
        self.connection._rollback_impl()
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1132, in _rollback_impl
        self._handle_dbapi_exception(e, None, None, None, None)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
        raise exc_info[1].with_traceback(exc_info[2])
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1130, in _rollback_impl
        self.engine.dialect.do_rollback(self.connection)
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
    File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 712, in do_rollback
        dbapi_connection.rollback()
        ~~~~~~~~~~~~~~~~~~~~~~~~~^^
    pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
    ```
</details>

5)
```
wrk -t2 -c5 -d15s http://localhost:8000/users
Running 15s test @ http://localhost:8000/users
  2 threads and 5 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.41s   356.73ms   1.92s    75.76%
    Req/Sec     1.55      2.11    10.00     90.91%
  37 requests in 15.02s, 71.77KB read
  Socket errors: connect 0, read 1, write 0, timeout 4
  Non-2xx or 3xx responses: 1
Requests/sec:      2.46
Transfer/sec:      4.78KB
```

Errors logs:
<details>
 ```
 INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53898 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53860 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200

thread '<unnamed>' panicked at src/lib.rs:220:65:
called `Option::unwrap()` on a `None` value
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
     ERROR   Exception in ASGI application
Traceback (most recent call last):
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
    await super().__call__(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
    await route.handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
    await super().handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 136, in app
    response = await f(request)
               ^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 690, in app
    raw_response = await run_endpoint_function(
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<3 lines>...
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 346, in run_endpoint_function
    return await run_in_threadpool(dependant.call, **values)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/concurrency.py", line 34, in run_in_threadpool
    return await anyio.to_thread.run_sync(func)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
    result = context.run(func, *args)
  File "/home/tinker/programming/libsql-demo/main.py", line 129, in fetch_users
    users = db.execute(select(User).order_by(User.id)).scalars().all()
            ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2373, in execute
    return self._execute_internal(
           ~~~~~~~~~~~~~~~~~~~~~~^
        statement,
        ^^^^^^^^^^
    ...<4 lines>...
        _add_event=_add_event,
        ^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2271, in _execute_internal
    result: Result[Any] = compile_state_cls.orm_execute_statement(
                          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self,
        ^^^^^
    ...<4 lines>...
        conn,
        ^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/context.py", line 306, in orm_execute_statement
    result = conn.execute(
        statement, params or {}, execution_options=execution_options
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1421, in execute
    return meth(
        self,
        distilled_parameters,
        execution_options or NO_OPTIONS,
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/sql/elements.py", line 526, in _execute_on_connection
    return connection._execute_clauseelement(
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        self, distilled_params, execution_options
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1643, in _execute_clauseelement
    ret = self._execute_context(
        dialect,
    ...<8 lines>...
        cache_hit=cache_hit,
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1823, in _execute_context
    self._handle_dbapi_exception(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        e, str(statement), parameters, None, None
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1817, in _execute_context
    context = constructor(
        dialect, self, conn, execution_options, *args, **kw
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 1438, in _init_compiled
    self.cursor = self.create_cursor()
                  ~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 1777, in create_cursor
    return self.create_default_cursor()
           ~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 1783, in create_default_cursor
    return self._dbapi_connection.cursor()
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 1494, in cursor
    return self.dbapi_connection.cursor(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
      INFO   127.0.0.1:53860 - "GET /users HTTP/1.1" 500
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53898 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53908 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53898 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53908 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53898 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53908 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53898 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53908 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53898 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53908 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53908 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53898 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200

thread '<unnamed>' panicked at src/lib.rs:260:42:
called `Option::unwrap()` on a `None` value
     ERROR   Exception in ASGI application
Traceback (most recent call last):
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
    await super().__call__(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
    await route.handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
    await super().handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 132, in app
    async with AsyncExitStack() as request_stack:
               ~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/contextlib.py", line 768, in __aexit__
    raise exc
  File "/usr/lib/python3.13/contextlib.py", line 751, in __aexit__
    cb_suppress = await cb(*exc_details)
                  ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/contextlib.py", line 221, in __aexit__
    await anext(self.gen)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/concurrency.py", line 39, in contextmanager_in_threadpool
    await anyio.to_thread.run_sync(
        cm.__exit__, None, None, None, limiter=exit_limiter
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
    result = context.run(func, *args)
  File "/usr/lib/python3.13/contextlib.py", line 148, in __exit__
    next(self.gen)
    ~~~~^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/main.py", line 84, in get_db
    db.close()
    ~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2529, in close
    self._close_impl(invalidate=False)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2598, in _close_impl
    transaction.close(invalidate)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "<string>", line 2, in close
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 1422, in close
    transaction.close()
    ~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2599, in close
    self._do_close()
    ~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2737, in _do_close
    self._close_impl()
    ~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2723, in _close_impl
    self._connection_rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2715, in _connection_rollback_impl
    self.connection._rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1132, in _rollback_impl
    self._handle_dbapi_exception(e, None, None, None, None)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1130, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 712, in do_rollback
    dbapi_connection.rollback()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53908 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53884 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:51040 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53870 - "GET /users HTTP/1.1" 200
      INFO   127.0.0.1:53908 - "GET /users HTTP/1.1" 200

thread '<unnamed>' panicked at src/lib.rs:260:42:
called `Option::unwrap()` on a `None` value
     ERROR   Exception in ASGI application
Traceback (most recent call last):
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
    await super().__call__(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
    await route.handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
    await super().handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 132, in app
    async with AsyncExitStack() as request_stack:
               ~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/contextlib.py", line 768, in __aexit__
    raise exc
  File "/usr/lib/python3.13/contextlib.py", line 751, in __aexit__
    cb_suppress = await cb(*exc_details)
                  ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/contextlib.py", line 221, in __aexit__
    await anext(self.gen)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/concurrency.py", line 39, in contextmanager_in_threadpool
    await anyio.to_thread.run_sync(
        cm.__exit__, None, None, None, limiter=exit_limiter
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
    result = context.run(func, *args)
  File "/usr/lib/python3.13/contextlib.py", line 148, in __exit__
    next(self.gen)
    ~~~~^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/main.py", line 84, in get_db
    db.close()
    ~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2529, in close
    self._close_impl(invalidate=False)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2598, in _close_impl
    transaction.close(invalidate)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "<string>", line 2, in close
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 1422, in close
    transaction.close()
    ~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2599, in close
    self._do_close()
    ~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2737, in _do_close
    self._close_impl()
    ~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2723, in _close_impl
    self._connection_rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2715, in _connection_rollback_impl
    self.connection._rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1132, in _rollback_impl
    self._handle_dbapi_exception(e, None, None, None, None)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1130, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 712, in do_rollback
    dbapi_connection.rollback()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value

thread '<unnamed>' panicked at src/lib.rs:260:42:
called `Option::unwrap()` on a `None` value

thread '<unnamed>' panicked at src/lib.rs:260:42:
called `Option::unwrap()` on a `None` value
     ERROR   Exception in ASGI application
Traceback (most recent call last):
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
    await super().__call__(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
    await route.handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
    await super().handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 132, in app
    async with AsyncExitStack() as request_stack:
               ~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/contextlib.py", line 768, in __aexit__
    raise exc
  File "/usr/lib/python3.13/contextlib.py", line 751, in __aexit__
    cb_suppress = await cb(*exc_details)
                  ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/contextlib.py", line 221, in __aexit__
    await anext(self.gen)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/concurrency.py", line 39, in contextmanager_in_threadpool
    await anyio.to_thread.run_sync(
        cm.__exit__, None, None, None, limiter=exit_limiter
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
    result = context.run(func, *args)
  File "/usr/lib/python3.13/contextlib.py", line 148, in __exit__
    next(self.gen)
    ~~~~^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/main.py", line 84, in get_db
    db.close()
    ~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2529, in close
    self._close_impl(invalidate=False)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2598, in _close_impl
    transaction.close(invalidate)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "<string>", line 2, in close
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 1422, in close
    transaction.close()
    ~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2599, in close
    self._do_close()
    ~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2737, in _do_close
    self._close_impl()
    ~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2723, in _close_impl
    self._connection_rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2715, in _connection_rollback_impl
    self.connection._rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1132, in _rollback_impl
    self._handle_dbapi_exception(e, None, None, None, None)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1130, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 712, in do_rollback
    dbapi_connection.rollback()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
     ERROR   Exception in ASGI application
Traceback (most recent call last):
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
    await super().__call__(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
    await route.handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
    await super().handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 132, in app
    async with AsyncExitStack() as request_stack:
               ~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/contextlib.py", line 768, in __aexit__
    raise exc
  File "/usr/lib/python3.13/contextlib.py", line 751, in __aexit__
    cb_suppress = await cb(*exc_details)
                  ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/contextlib.py", line 221, in __aexit__
    await anext(self.gen)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/concurrency.py", line 39, in contextmanager_in_threadpool
    await anyio.to_thread.run_sync(
        cm.__exit__, None, None, None, limiter=exit_limiter
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
    result = context.run(func, *args)
  File "/usr/lib/python3.13/contextlib.py", line 148, in __exit__
    next(self.gen)
    ~~~~^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/main.py", line 84, in get_db
    db.close()
    ~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2529, in close
    self._close_impl(invalidate=False)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2598, in _close_impl
    transaction.close(invalidate)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "<string>", line 2, in close
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 1422, in close
    transaction.close()
    ~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2599, in close
    self._do_close()
    ~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2737, in _do_close
    self._close_impl()
    ~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2723, in _close_impl
    self._connection_rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2715, in _connection_rollback_impl
    self.connection._rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1132, in _rollback_impl
    self._handle_dbapi_exception(e, None, None, None, None)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1130, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 712, in do_rollback
    dbapi_connection.rollback()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
    ```
    ```
</details>

---

### Logs with enabled RUST_BACKTRACE

**Used `export RUST_BACKTRACE=1` to enable detailed rust error traces**

```
wrk -t2 -c5 -d15s http://localhost:8000/users
Running 15s test @ http://localhost:8000/users
  2 threads and 5 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.94s    72.66ms   1.99s    72.73%
    Req/Sec     0.08      0.28     1.00     92.31%
  21 requests in 15.02s, 41.75KB read
  Socket errors: connect 0, read 2, write 0, timeout 10
Requests/sec:      1.40
Transfer/sec:      2.78KB
```

**Error logs:**
<details>
```
pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
INFO:     127.0.0.1:41490 - "GET /users HTTP/1.1" 200 OK
INFO:     127.0.0.1:41514 - "GET /users HTTP/1.1" 200 OK
INFO:     127.0.0.1:41504 - "GET /users HTTP/1.1" 200 OK
INFO:     127.0.0.1:41496 - "GET /users HTTP/1.1" 200 OK

thread '<unnamed>' panicked at src/lib.rs:260:42:
called `Option::unwrap()` on a `None` value
stack backtrace:
   0:     0x7a28a73a8062 - <std::sys::backtrace::BacktraceLock::print::DisplayBacktrace as core::fmt::Display>::fmt::hc04c8f544ab24d66
   1:     0x7a28a73cf423 - core::fmt::write::hfe57b7174b7d8eab
   2:     0x7a28a73a4bb3 - std::io::Write::write_fmt::h154385efa8565236
   3:     0x7a28a73a7eb2 - std::sys::backtrace::BacktraceLock::print::h0c8f24e22f5873a8
   4:     0x7a28a73a8f12 - std::panicking::default_hook::{{closure}}::hd07d57e6a602c8e4
   5:     0x7a28a73a8d15 - std::panicking::default_hook::h63d12f7d95bd91ed
   6:     0x7a28a73a98b2 - std::panicking::rust_panic_with_hook::h33b18b24045abff4
   7:     0x7a28a73a9626 - std::panicking::begin_panic_handler::{{closure}}::hf8313cc2fd0126bc
   8:     0x7a28a73a8569 - std::sys::backtrace::__rust_end_short_backtrace::h57fe07c8aea5c98a
   9:     0x7a28a73a92ed - __rustc[95feac21a9532783]::rust_begin_unwind
  10:     0x7a28a6ca2f60 - core::panicking::panic_fmt::hd54fb667be51beea
  11:     0x7a28a6ca2fec - core::panicking::panic::h48a7e1f3665210c6
  12:     0x7a28a6ca2ed9 - core::option::unwrap_failed::haa1cd4d2df4f1dcb
  13:     0x7a28a6d9520d - libsql_experimental::_::<impl libsql_experimental::Connection>::__pymethod_rollback__::h8490841bc4d39f1b
  14:     0x7a28a6d8d990 - pyo3::impl_::trampoline::trampoline::h5554fd471c4924f9
  15:     0x7a28a6d94180 - libsql_experimental::_::<impl pyo3::impl_::pyclass::PyMethods<libsql_experimental::Connection> for pyo3::impl_::pyclass::PyClassImplCollector<libsql_experimental::Connection>>::py_methods::ITEMS::trampoline::h13c3c3bcf5b12c9e
  16:           0x55d338 - <unknown>
  17:           0x55c143 - PyObject_Vectorcall
  18:           0x572017 - _PyEval_EvalFrameDefault
  19:           0x62b1ce - <unknown>
  20:           0x5724c4 - _PyEval_EvalFrameDefault
  21:           0x5e3e77 - <unknown>
  22:           0x6df05d - <unknown>
  23:           0x71b20a - <unknown>
  24:           0x58faa4 - <unknown>
  25:           0x5752f3 - _PyEval_EvalFrameDefault
  26:           0x5e3ded - <unknown>
  27:           0x6fe727 - <unknown>
  28:           0x6a764c - <unknown>
  29:     0x7a28ab0a3d64 - start_thread
                               at ./nptl/pthread_create.c:448:8
  30:     0x7a28ab1373fc - __GI___clone3
                               at ./misc/../sysdeps/unix/sysv/linux/x86_64/clone3.S:78:0
  31:                0x0 - <unknown>
ERROR:    Exception in ASGI application
Traceback (most recent call last):
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/protocols/http/httptools_impl.py", line 422, in run_asgi
    result = await app(  # type: ignore[func-returns-value]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        self.scope, self.receive, self.send
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/uvicorn/middleware/proxy_headers.py", line 63, in __call__
    return await self.app(scope, receive, send)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/applications.py", line 1163, in __call__
    await super().__call__(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/applications.py", line 90, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/errors.py", line 164, in __call__
    await self.app(scope, receive, _send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/middleware/exceptions.py", line 63, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/middleware/asyncexitstack.py", line 18, in __call__
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 660, in __call__
    await self.middleware_stack(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 2683, in app
    await route.handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 1266, in handle
    await super().handle(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/routing.py", line 276, in handle
    await self.app(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 150, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/starlette/_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/routing.py", line 132, in app
    async with AsyncExitStack() as request_stack:
               ~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/contextlib.py", line 768, in __aexit__
    raise exc
  File "/usr/lib/python3.13/contextlib.py", line 751, in __aexit__
    cb_suppress = await cb(*exc_details)
                  ^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/contextlib.py", line 221, in __aexit__
    await anext(self.gen)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/fastapi/concurrency.py", line 39, in contextmanager_in_threadpool
    await anyio.to_thread.run_sync(
        cm.__exit__, None, None, None, limiter=exit_limiter
    )
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/to_thread.py", line 63, in run_sync
    return await get_async_backend().run_sync_in_worker_thread(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        func, args, abandon_on_cancel=abandon_on_cancel, limiter=limiter
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 2596, in run_sync_in_worker_thread
    return await future
           ^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/anyio/_backends/_asyncio.py", line 1029, in run
    result = context.run(func, *args)
  File "/usr/lib/python3.13/contextlib.py", line 148, in __exit__
    next(self.gen)
    ~~~~^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/main.py", line 84, in get_db
    db.close()
    ~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2529, in close
    self._close_impl(invalidate=False)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 2598, in _close_impl
    transaction.close(invalidate)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^
  File "<string>", line 2, in close
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py", line 137, in _go
    ret_value = fn(self, *arg, **kw)
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/orm/session.py", line 1422, in close
    transaction.close()
    ~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2599, in close
    self._do_close()
    ~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2737, in _do_close
    self._close_impl()
    ~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2723, in _close_impl
    self._connection_rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2715, in _connection_rollback_impl
    self.connection._rollback_impl()
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1132, in _rollback_impl
    self._handle_dbapi_exception(e, None, None, None, None)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2368, in _handle_dbapi_exception
    raise exc_info[1].with_traceback(exc_info[2])
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 1130, in _rollback_impl
    self.engine.dialect.do_rollback(self.connection)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/home/tinker/programming/libsql-demo/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 712, in do_rollback
    dbapi_connection.rollback()
    ~~~~~~~~~~~~~~~~~~~~~~~~~^^
pyo3_runtime.PanicException: called `Option::unwrap()` on a `None` value
INFO:     127.0.0.1:41490 - "GET /users HTTP/1.1" 200 OK
```
</details>

---

### Testing with `NullPool` configuration of sqlalchemy

```
wrk -t2 -c5 -d15s http://localhost:8000/users
Running 15s test @ http://localhost:8000/users
  2 threads and 5 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     0.00us    0.00us   0.00us    -nan%
    Req/Sec     0.00      0.00     0.00    100.00%
  20 requests in 15.02s, 39.77KB read
  Socket errors: connect 0, read 0, write 0, timeout 20
Requests/sec:      1.33
Transfer/sec:      2.65KB
```

Result: Only timeouts are observed, no panics or errors were seen in server logs.
