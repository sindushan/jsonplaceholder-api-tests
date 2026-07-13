"""Reusable assertion helpers to keep tests readable and failures descriptive."""

import re

import requests

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
URL_PATTERN = re.compile(r"^https?://")


def assert_status(response: requests.Response, expected: int) -> None:
    assert response.status_code == expected, (
        f"{response.request.method} {response.url} -> "
        f"expected {expected}, got {response.status_code}. Body: {response.text[:300]}"
    )


def assert_json_content_type(response: requests.Response) -> None:
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, (
        f"Expected JSON content type, got '{content_type}'"
    )


def assert_schema(item: dict, schema: dict) -> None:
    """Validate that `item` contains every field in `schema` with the expected type.

    `schema` maps field name -> expected Python type, e.g. {"id": int, "title": str}.
    """
    for field, expected_type in schema.items():
        assert field in item, f"Missing required field '{field}' in: {item}"
        actual = item[field]
        assert isinstance(actual, expected_type), (
            f"Field '{field}' expected type {expected_type.__name__}, "
            f"got {type(actual).__name__} (value: {actual!r})"
        )


def assert_valid_email(value: str) -> None:
    assert EMAIL_PATTERN.match(value), f"Invalid email format: {value!r}"


def assert_valid_url(value: str) -> None:
    assert URL_PATTERN.match(value), f"Invalid URL format: {value!r}"
