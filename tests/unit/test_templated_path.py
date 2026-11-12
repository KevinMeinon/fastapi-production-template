"""Unit tests for the metrics path templating helper."""

import pytest

from fastapi_production_template.middleware.request_id import _templated_path


@pytest.mark.parametrize(
    ("url_path", "template", "expected"),
    [
        # Newer FastAPI: route paths are relative to the router prefix.
        ("/api/v1/health", "/health", "/api/v1/health"),
        ("/api/v1/documents/doc-001", "/documents/{document_id}", "/api/v1/documents/{document_id}"),
        # Older FastAPI: route paths already carry the full prefix.
        ("/api/v1/health", "/api/v1/health", "/api/v1/health"),
        # Template longer than URL, or a non-matching URL: fall back to the literal URL.
        ("/health", "/api/v1/health", "/health"),
        ("/api/v1/other", "/health", "/api/v1/other"),
        # Root-level route.
        ("/", "/", "/"),
    ],
)
def test_templated_path(url_path: str, template: str, expected: str) -> None:
    assert _templated_path(url_path, template) == expected
