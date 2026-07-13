"""Shared pytest fixtures for the JSONPlaceholder API test suite."""

import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


class ApiClient:
    """Thin wrapper around requests.Session.

    Centralizes the base URL and default headers so individual tests
    only deal with relative paths. Keeping this minimal (rather than a
    full SDK-style client) is intentional given the time box.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs) -> requests.Response:
        return self.session.get(self._url(path), timeout=10, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self.session.post(self._url(path), timeout=10, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self.session.put(self._url(path), timeout=10, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.session.patch(self._url(path), timeout=10, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.session.delete(self._url(path), timeout=10, **kwargs)

    def close(self):
        self.session.close()


@pytest.fixture(scope="session")
def api() -> ApiClient:
    """Session-scoped API client so all tests reuse one TCP connection pool."""
    client = ApiClient(BASE_URL)
    yield client
    client.close()
