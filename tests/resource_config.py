"""Metadata describing every JSONPlaceholder resource.

This is the core of the suite's design: rather than duplicating near-identical
tests per route, common behaviors (list, get-by-id, 404s, delete) are
parameterized over this table. Adding a new resource means adding one entry.
"""

RESOURCES = {
    "posts": {
        "count": 100,
        "schema": {"userId": int, "id": int, "title": str, "body": str},
    },
    "comments": {
        "count": 500,
        "schema": {"postId": int, "id": int, "name": str, "email": str, "body": str},
    },
    "albums": {
        "count": 100,
        "schema": {"userId": int, "id": int, "title": str},
    },
    "photos": {
        "count": 5000,
        "schema": {
            "albumId": int,
            "id": int,
            "title": str,
            "url": str,
            "thumbnailUrl": str,
        },
    },
    "todos": {
        "count": 200,
        "schema": {"userId": int, "id": int, "title": str, "completed": bool},
    },
    "users": {
        "count": 10,
        "schema": {
            "id": int,
            "name": str,
            "username": str,
            "email": str,
            "address": dict,
            "phone": str,
            "website": str,
            "company": dict,
        },
    },
}

RESOURCE_NAMES = list(RESOURCES.keys())
