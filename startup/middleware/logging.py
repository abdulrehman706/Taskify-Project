from starlette.requests import Request
import time


class SimpleLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            start = time.time()
            await self.app(scope, receive, send)
            duration = time.time() - start
            print(f"{request.method} {request.url.path} completed in {duration:.3f}s")
        else:
            await self.app(scope, receive, send)
