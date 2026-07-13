"""Resource-specific data-quality tests that go beyond the common schema checks."""

import pytest

from utils.assertions import assert_status, assert_valid_email, assert_valid_url


class TestComments:
    def test_comment_emails_are_valid_format(self, api):
        response = api.get("/comments", params={"postId": 1})
        assert_status(response, 200)
        for comment in response.json():
            assert_valid_email(comment["email"])


class TestTodos:
    @pytest.mark.parametrize("completed", ["true", "false"])
    def test_filter_todos_by_completed(self, api, completed):
        response = api.get("/todos", params={"completed": completed})
        assert_status(response, 200)

        todos = response.json()
        assert len(todos) > 0
        expected = completed == "true"
        assert all(t["completed"] is expected for t in todos)

    def test_completed_and_pending_partition_full_set(self, api):
        """completed=true + completed=false should account for all 200 todos."""
        done = api.get("/todos", params={"completed": "true"}).json()
        pending = api.get("/todos", params={"completed": "false"}).json()
        assert len(done) + len(pending) == 200


class TestUsers:
    def test_user_emails_are_valid_format(self, api):
        response = api.get("/users")
        assert_status(response, 200)
        for user in response.json():
            assert_valid_email(user["email"])

    def test_user_address_contains_geo_coordinates(self, api):
        """Nested object validation: address.geo must hold parseable lat/lng."""
        response = api.get("/users/1")
        assert_status(response, 200)

        address = response.json()["address"]
        for field in ("street", "suite", "city", "zipcode", "geo"):
            assert field in address, f"Missing address field '{field}'"

        geo = address["geo"]
        # Values are strings in the API; they must parse as floats.
        float(geo["lat"])
        float(geo["lng"])

    def test_user_nested_route_albums(self, api):
        response = api.get("/users/1/albums")
        assert_status(response, 200)
        albums = response.json()
        assert len(albums) == 10, "Each seeded user has exactly 10 albums"
        assert all(a["userId"] == 1 for a in albums)


class TestPhotos:
    def test_photo_urls_are_valid_format(self, api):
        """Validate URL fields on a sample (first album) rather than all 5000."""
        response = api.get("/albums/1/photos")
        assert_status(response, 200)

        photos = response.json()
        assert len(photos) == 50, "Each seeded album has exactly 50 photos"
        for photo in photos:
            assert_valid_url(photo["url"])
            assert_valid_url(photo["thumbnailUrl"])
