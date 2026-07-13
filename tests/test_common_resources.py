"""Common behaviors tested across ALL six JSONPlaceholder resources.

Parameterizing over the resource table gives broad route coverage
(6 resources x N behaviors) without duplicated code.
"""

import pytest

from tests.resource_config import RESOURCES, RESOURCE_NAMES
from utils.assertions import assert_json_content_type, assert_schema, assert_status


@pytest.mark.smoke
@pytest.mark.parametrize("resource", RESOURCE_NAMES)
def test_list_returns_200_and_expected_count(api, resource):
    """GET /{resource} returns 200, JSON, and the documented record count."""
    response = api.get(f"/{resource}")

    assert_status(response, 200)
    assert_json_content_type(response)

    body = response.json()
    assert isinstance(body, list), f"Expected a JSON array, got {type(body).__name__}"
    expected = RESOURCES[resource]["count"]
    assert len(body) == expected, f"Expected {expected} {resource}, got {len(body)}"


@pytest.mark.smoke
@pytest.mark.parametrize("resource", RESOURCE_NAMES)
def test_get_by_id_returns_valid_schema(api, resource):
    """GET /{resource}/1 returns a single object matching the expected schema."""
    response = api.get(f"/{resource}/1")

    assert_status(response, 200)
    item = response.json()
    assert isinstance(item, dict)
    assert item["id"] == 1
    assert_schema(item, RESOURCES[resource]["schema"])


@pytest.mark.parametrize("resource", RESOURCE_NAMES)
def test_list_items_all_match_schema(api, resource):
    """Every item in the collection conforms to the resource schema."""
    response = api.get(f"/{resource}")
    assert_status(response, 200)

    for item in response.json():
        assert_schema(item, RESOURCES[resource]["schema"])


@pytest.mark.parametrize("resource", RESOURCE_NAMES)
def test_list_ids_are_unique_and_sequential(api, resource):
    """IDs in each collection are unique and run 1..count with no gaps."""
    response = api.get(f"/{resource}")
    assert_status(response, 200)

    ids = [item["id"] for item in response.json()]
    assert len(ids) == len(set(ids)), "Duplicate IDs found"
    assert ids == list(range(1, RESOURCES[resource]["count"] + 1))


@pytest.mark.negative
@pytest.mark.parametrize("resource", RESOURCE_NAMES)
def test_get_nonexistent_id_returns_404(api, resource):
    """GET /{resource}/<id beyond range> returns 404 with an empty JSON body."""
    beyond_range = RESOURCES[resource]["count"] + 1
    response = api.get(f"/{resource}/{beyond_range}")

    assert_status(response, 404)
    assert response.json() == {}, "JSONPlaceholder returns an empty object on 404"


@pytest.mark.negative
@pytest.mark.parametrize("bad_id", ["0", "-1", "abc"])
def test_get_invalid_id_formats_return_404(api, bad_id):
    """Invalid ID formats (zero, negative, non-numeric) return 404.

    Run against /posts as a representative resource to limit runtime.
    """
    response = api.get(f"/posts/{bad_id}")
    assert_status(response, 404)


@pytest.mark.crud
@pytest.mark.parametrize("resource", RESOURCE_NAMES)
def test_delete_returns_200(api, resource):
    """DELETE /{resource}/1 returns 200 (API fakes deletion, does not persist)."""
    response = api.delete(f"/{resource}/1")
    assert_status(response, 200)


@pytest.mark.negative
def test_unknown_route_returns_404(api):
    """Routes that don't exist at all return 404."""
    response = api.get("/nonexistent-resource")
    assert_status(response, 404)
