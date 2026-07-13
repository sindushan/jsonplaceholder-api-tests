"""Smoke test: verify the API is reachable and the client fixture works."""

import pytest


@pytest.mark.smoke
def test_api_is_reachable(api):
    """GET /posts should return 200 — confirms base URL, session, and fixture wiring."""
    response = api.get("/posts")
    assert response.status_code == 200
    assert response.json(), "expected a non-empty list of posts"
