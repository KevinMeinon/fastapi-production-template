"""Request id middleware and context utilities."""

from contextvars import ContextVar
from time import perf_counter
from uuid import uuid4

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
from starlette.types import ASGIApp

from fastapi_production_template.observability.metrics import MetricsStore

_request_id_ctx: ContextVar[str | None] = ContextVar("request_id", default=None)


def get_request_id() -> str | None:
    """Read request id from context."""

    return _request_id_ctx.get()


def _templated_path(url_path: str, template: str) -> str:
    """Rebuild the full templated path from a URL and a (possibly mount-relative) route template.

    FastAPI's newer router inclusion stores route paths relative to their router prefix
    (e.g. ``/health`` for a route mounted at ``/api/v1``). Re-anchor the template to the
    actual URL so metrics labels keep the full path and stay cardinality-safe.
    """

    url_parts = [part for part in url_path.split("/") if part]
    template_parts = [part for part in template.split("/") if part]
    offset = len(url_parts) - len(template_parts)
    if offset < 0:
        return url_path
    for url_part, template_part in zip(url_parts[offset:], template_parts, strict=True):
        if url_part != template_part and not template_part.startswith("{"):
            return url_path
    if not offset:
        return template
    return "/" + "/".join([*url_parts[:offset], *template_parts])


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach request id to context, response, logs, and metrics."""

    def __init__(self, app: ASGIApp, *, metrics: MetricsStore) -> None:
        super().__init__(app)
        self._metrics = metrics

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        token = _request_id_ctx.set(request_id)
        route_path = request.url.path

        start = perf_counter()
        self._metrics.increment_in_flight()
        response: StarletteResponse
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            route = request.scope.get("route")
            if route is not None and hasattr(route, "path"):
                route_path = _templated_path(request.url.path, str(route.path))
        finally:
            duration = perf_counter() - start
            self._metrics.observe(
                method=request.method,
                path=route_path,
                status_code=status_code,
                duration_seconds=duration,
            )
            self._metrics.decrement_in_flight()

        response.headers["X-Request-ID"] = request_id
        logger.info("{} {} {}", request.method, request.url.path, response.status_code)
        _request_id_ctx.reset(token)
        return response
