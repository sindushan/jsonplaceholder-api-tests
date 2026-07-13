"""In-depth tests for /posts: full CRUD lifecycle, query filters, nested routes.

Posts is used as the representative resource for write operations since
JSONPlaceholder handles POST/PUT/PATCH identically across resources.
"""

import pytest

from utils.assertions import assert_status


@pytest.mark.crud
def test_create_post_returns_201_and_echoes_payload(api):
    payload = {"title": "Test title", "body": "Test body", "userId": 1}
    response = api.post("/posts", json=payload)

    assert_status(response, 201)
    created = response.json()
    # API assigns the next available ID (101) but does not persist.
    assert created["id"] == 101
    for key, value in payload.items():
        assert created[key] == value, f"Field '{key}' not echoed back correctly"


@pytest.mark.crud
def test_full_update_with_put_returns_200(api):
    payload = {"id": 1, "title": "Updated", "body": "Updated body", "userId": 1}
    response = api.put("/posts/1", json=payload)

    assert_status(response, 200)
    updated = response.json()
    assert updated["title"] == "Updated"
    assert updated["body"] == "Updated body"


@pytest.mark.crud
def test_partial_update_with_patch_returns_200(api):
    response = api.patch("/posts/1", json={"title": "Patched title"})

    assert_status(response, 200)
    assert response.json()["title"] == "Patched title"


@pytest.mark.crud
def test_create_post_with_empty_body_still_returns_201(api):
    """Documents a known API quirk: no input validation, empty POST succeeds.

    In a real system this would likely be a 400; the test pins current behavior.
    """
    response = api.post("/posts", json={})
    assert_status(response, 201)
    assert response.json() == {"id": 101}


@pytest.mark.parametrize("user_id", [1, 5, 10])
def test_filter_posts_by_user_id(api, user_id):
    response = api.get("/posts", params={"userId": user_id})

    assert_status(response, 200)
    posts = response.json()
    assert len(posts) == 10, "Each seeded user has exactly 10 posts"
    assert all(p["userId"] == user_id for p in posts)


def test_filter_by_nonexistent_user_returns_empty_list(api):
    response = api.get("/posts", params={"userId": 9999})
    assert_status(response, 200)
    assert response.json() == []


def test_nested_route_post_comments(api):
    """GET /posts/1/comments returns only comments belonging to post 1."""
    response = api.get("/posts/1/comments")

    assert_status(response, 200)
    comments = response.json()
    assert len(comments) == 5, "Each seeded post has exactly 5 comments"
    assert all(c["postId"] == 1 for c in comments)


def test_nested_route_matches_query_filter(api):
    """Nested route and equivalent query-param filter return the same data."""
    nested = api.get("/posts/1/comments").json()
    filtered = api.get("/comments", params={"postId": 1}).json()
    assert nested == filtered
