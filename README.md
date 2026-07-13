# JSONPlaceholder API Test Automation

[![API Tests](https://github.com/sindushan/jsonplaceholder-api-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/sindushan/jsonplaceholder-api-tests/actions/workflows/tests.yml)

Automated API test suite for [JSONPlaceholder](https://jsonplaceholder.typicode.com), built with **Python + pytest + requests** for the SDET technical assessment.

## Overview

The suite covers all six JSONPlaceholder resources (`/posts`, `/comments`, `/albums`, `/photos`, `/todos`, `/users`) using a **data-driven design**: resource metadata (expected record counts and field schemas) lives in a single table (`tests/resource_config.py`), and common behaviors are parameterized over it. This keeps the code DRY, makes failures descriptive, and means adding a new resource requires one dictionary entry rather than a new test file.

The full suite is **59 tests** and runs in a few seconds.

### Project structure

```
├── conftest.py                     # Session-scoped ApiClient fixture (base URL, timeouts, connection reuse)
├── pytest.ini                      # Test discovery config + custom markers
├── requirements.txt
├── utils/
│   └── assertions.py               # Reusable assertion helpers (status, schema, email/URL format)
└── tests/
    ├── resource_config.py          # Central resource metadata (counts + schemas)
    ├── test_smoke.py               # Fast reachability check (API is up, fixture wired)
    ├── test_common_resources.py    # Behaviors parameterized across all 6 resources
    ├── test_posts.py               # CRUD lifecycle, filters, nested routes
    └── test_resource_specific.py   # Data-quality tests per resource
```

### Assumptions

- JSONPlaceholder is a stable, seeded dataset: record counts (100 posts, 500 comments, 100 albums, 5000 photos, 200 todos, 10 users) are fixed and safe to assert on.
- Write operations (POST/PUT/PATCH/DELETE) are faked by the API — they return success responses but do not persist. Tests therefore validate the *response contract* (status codes, echoed payloads, assigned IDs) rather than persistence.
- The API performs no input validation (e.g., an empty POST body returns 201). Tests pin this current behavior and document it, rather than treating it as a failure.
- No authentication is required; no auth scenarios apply.
- Tests are read-safe and idempotent, so they can run in any order and in parallel.

## Execution Instructions

Requires Python 3.9+.

```bash
# 1. Clone and enter the repo
git clone https://github.com/sindushan/jsonplaceholder-api-tests.git
cd jsonplaceholder-api-tests

# 2. Create a virtual environment and install dependencies
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 3. Run the full suite
pytest

# Run only a subset via markers
pytest -m smoke        # fast health checks
pytest -m crud         # create/update/delete lifecycle
pytest -m negative     # error handling / invalid input

# 4. Generate an HTML report
pytest --html=report.html --self-contained-html
```

**Targeting another environment:** the base URL is read from the `API_BASE_URL`
environment variable (defaulting to the public instance), so the same suite can
run against a local mock or staging server:

```bash
API_BASE_URL=http://localhost:3000 pytest
```

## Continuous Integration

A [GitHub Actions workflow](.github/workflows/tests.yml) runs the full suite on a
clean Ubuntu machine on every push and pull request to `main`, and archives the
HTML report as a build artifact. Live status is shown by the badge at the top.

**Viewing results:** pytest prints verbose pass/fail output to the console (configured in `pytest.ini`). For a shareable report, open `report.html` in a browser after running the report command above.

## Coverage Summary

### Routes/resources tested

All six resources, via parameterization: `/posts`, `/comments`, `/albums`, `/photos`, `/todos`, `/users`, plus nested routes (`/posts/{id}/comments`, `/users/{id}/albums`, `/albums/{id}/photos`) and query-parameter filtering (`?userId=`, `?postId=`, `?completed=`).

### Validations implemented

- **Status codes** — 200/201 on success, 404 for missing IDs, invalid ID formats, and unknown routes.
- **Response schema** — required fields and correct JSON types for every item in every collection, including nested objects (`users.address.geo`).
- **Data integrity** — expected record counts; unique, gap-free sequential IDs; filter results actually match the filter; nested routes are consistent with equivalent query filters; completed/pending todos partition the full set.
- **Format validation** — email format on comments and users, URL format on photos.
- **CRUD contract** — POST returns 201 with assigned ID and echoed payload; PUT/PATCH return 200 with updated fields; DELETE returns 200.
- **Negative cases** — out-of-range IDs, zero/negative/non-numeric IDs, nonexistent routes, filtering by a nonexistent foreign key, empty POST body (documents the API's lack of input validation).
- **Headers** — `Content-Type: application/json` on responses.

### Intentionally omitted due to time constraints

- Performance/load testing and response-time SLAs.
- Concurrency/race-condition scenarios (not meaningful against a non-persisting fake API).
- Exhaustive per-record validation of all 5,000 photos (sampled one album instead).
- HTTP-level edge cases (malformed JSON bodies, unsupported methods like OPTIONS/HEAD, header fuzzing).
- Contract testing against a formal OpenAPI spec (none is published for this API).
