# FastAPI Template

A reusable, production-ready FastAPI boilerplate that gives teams a strong starting point for future API projects. The template includes JWT authentication, async SQLAlchemy, PostgreSQL-ready configuration, Alembic migrations, clear API docs, and tests that are easy for other developers to extend.

## Features

- FastAPI application factory-style setup in a simple, modular layout
- JWT authentication with secure password hashing using Argon2 via `pwdlib`
- User registration and login with bearer token protection
- Role-based access control with `user` and `admin` examples
- Pydantic validation for request payloads, email formatting, and password strength
- Async SQLAlchemy with PostgreSQL-ready configuration
- Reusable timestamp mixin for `created_at` and `updated_at`
- User model with `id`, `email`, `password_hash`, `full_name`, role, and activity status
- Connection pooling controls for async PostgreSQL deployments
- Environment-based security settings and configurable CORS middleware
- Global exception handlers with a standardized error response format
- Structured request logging with JSON output and request IDs
- Environment-aware log levels for local and non-local deployments
- Alembic migrations for controlled schema evolution
- Versioned API routing under `/api/v1`
- Health endpoint for smoke checks and readiness probes
- Auto-generated Swagger and OpenAPI docs with endpoint descriptions and schema examples
- `pytest` test coverage for the auth flow and access control
- `ruff` configuration for linting and formatting

## Project structure

```text
.
|-- app
|   |-- api
|   |   |-- dependencies
|   |   `-- v1
|   |       `-- endpoints
|   |-- core
|   |-- db
|   |   `-- models
|   |-- schemas
|   |-- scripts
|   |-- services
|   `-- main.py
|-- tests
|   `-- api
|       `-- v1
|-- alembic
|   `-- versions
|-- .env.example
|-- alembic.ini
|-- pyproject.toml
`-- README.md
```

## Quick start

1. Create a virtual environment.
2. Install dependencies.
3. Copy `.env.example` to `.env`.
4. Create a PostgreSQL database and update `.env` if needed.
5. Apply database migrations.
6. Optionally seed the default admin account.
7. Run the app.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
alembic upgrade head
seed-admin
uvicorn app.main:app --reload
```

macOS and Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
alembic upgrade head
seed-admin
uvicorn app.main:app --reload
```

Open the following URLs after startup:

- App: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/api/v1/health`

## Database layer

The template uses async SQLAlchemy sessions for application code and targets PostgreSQL via `asyncpg`. Tests use in-memory SQLite through `aiosqlite` so contributors can run the suite without provisioning a database server.

Key pieces:

- `app/db/session.py`: async engine, connection pooling, and session management
- `app/db/base.py`: declarative base plus reusable timestamp mixin
- `app/db/models/user.py`: async-compatible ORM user model
- `alembic/`: schema migration history

## Database migrations

Alembic is included so schema changes are tracked explicitly instead of relying on the API process to manage schema state on startup.

Apply the current schema:

```bash
alembic upgrade head
```

Create a new migration after model changes:

```bash
alembic revision --autogenerate -m "describe your change"
```

Roll back one migration:

```bash
alembic downgrade -1
```

The application does not create or mutate tables on startup. Run migrations explicitly before starting the API in local, staging, and production environments.

## Admin bootstrap

The template does not create privileged users automatically during API startup. If you want the sample admin account defined by `APP_DEFAULT_ADMIN_EMAIL` and `APP_DEFAULT_ADMIN_PASSWORD`, run:

```bash
seed-admin
```

This keeps normal app startup side-effect free while still giving teams a simple bootstrap path for development environments.

## Security features

The template includes a few baseline production-minded security practices out of the box:

- email validation via `EmailStr`
- password strength validation during account creation
- JWT-based authentication and role checks
- CORS configured through environment variables
- environment-based secrets and admin bootstrap credentials instead of runtime hardcoded values

Password rules for account creation:

- at least 8 characters
- at least one uppercase letter
- at least one lowercase letter
- at least one number
- at least one special character

## Error handling and logging

The template now includes a consistent error and logging layer suitable for extension in real projects:

- global exception handlers for validation errors, HTTP errors, and unexpected server errors
- a standardized error response envelope across endpoints
- per-request `X-Request-ID` headers for both success and error responses
- structured request logs with JSON output by default
- environment-aware log levels, with `DEBUG` as the default in `local` and `INFO` elsewhere unless overridden

Standard error response format:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Request validation failed.",
    "request_id": "2ee56d4b-859b-426d-9f0b-23ec6cc8db4b",
    "details": [
      {
        "field": "body.email",
        "message": "value is not a valid email address",
        "type": "value_error"
      }
    ]
  }
}
```

Typical error codes returned by the template include:

- `validation_error`
- `unauthorized`
- `forbidden`
- `not_found`
- `conflict`
- `internal_server_error`

Request logs include fields such as:

- `timestamp`
- `level`
- `logger`
- `message`
- `request_id`
- `method`
- `path`
- `status_code`
- `duration_ms`
- `client_ip`

## Environment variables

All application settings are namespaced with `APP_` to avoid collisions with machine-level variables.

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_NAME` | Human-readable API name | `FastAPI Template` |
| `APP_ENV` | Environment label for responses and config | `local` |
| `APP_DEBUG` | FastAPI debug mode | `false` |
| `APP_API_V1_PREFIX` | Prefix for version 1 routes | `/api/v1` |
| `APP_VERSION` | API version shown in docs | `0.1.0` |
| `APP_DATABASE_URL` | Async SQLAlchemy database URL | Required |
| `APP_DB_POOL_SIZE` | Base PostgreSQL connection pool size | `10` |
| `APP_DB_MAX_OVERFLOW` | Extra pooled connections allowed above the base pool | `20` |
| `APP_DB_POOL_TIMEOUT` | Seconds to wait for a pooled connection | `30` |
| `APP_DB_POOL_RECYCLE` | Seconds before recycling a pooled PostgreSQL connection | `1800` |
| `APP_SECRET_KEY` | JWT signing secret | Required, minimum 32 characters |
| `APP_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes | `30` |
| `APP_LOG_LEVEL` | Optional override for the application log level | `DEBUG` in `local`, `INFO` otherwise |
| `APP_LOG_JSON` | Whether logs should be emitted as structured JSON | `true` |
| `APP_CORS_ALLOW_ORIGINS` | Comma-separated allowed origins for browser clients | `http://localhost:3000,http://127.0.0.1:3000` |
| `APP_CORS_ALLOW_CREDENTIALS` | Whether browsers may send credentials on cross-origin requests | `true` |
| `APP_CORS_ALLOW_METHODS` | Comma-separated HTTP methods exposed by CORS | `GET,POST,PUT,PATCH,DELETE,OPTIONS` |
| `APP_CORS_ALLOW_HEADERS` | Comma-separated allowed request headers for CORS | `Authorization,Content-Type` |
| `APP_DEFAULT_ADMIN_EMAIL` | Optional seeded admin account email, used by `seed-admin` | Not set |
| `APP_DEFAULT_ADMIN_PASSWORD` | Optional seeded admin password, used by `seed-admin` | Not set |

`APP_DATABASE_URL` and `APP_SECRET_KEY` must be supplied through the environment or `.env`. If you want to use `seed-admin`, provide both `APP_DEFAULT_ADMIN_EMAIL` and `APP_DEFAULT_ADMIN_PASSWORD` together.

## Authentication flow

### Register

`POST /api/v1/users`

```json
{
  "full_name": "Priya Sharma",
  "email": "priya.sharma@example.com",
  "password": "StrongPassword123!"
}
```

### Login

`POST /api/v1/auth/tokens`

```json
{
  "email": "priya.sharma@example.com",
  "password": "StrongPassword123!"
}
```

The response returns a JWT access token:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.example",
  "token_type": "bearer"
}
```

Use it in protected requests:

```text
Authorization: Bearer <access_token>
```

Validation and auth failures also appear in the Swagger docs with the shared error schema and examples.

## Protected routes

- `GET /api/v1/users/current`: any authenticated user
- `GET /api/v1/admin/overview`: admin role only

Use `seed-admin` if you want to create the default admin account from `APP_DEFAULT_ADMIN_EMAIL` and `APP_DEFAULT_ADMIN_PASSWORD`.

## Run tests

```bash
pytest
```

The tests cover:

- health endpoint availability
- user registration
- successful login
- standardized error response formatting
- password strength validation
- email format validation
- CORS preflight behavior
- protected route access
- role-based access control
- invalid credential handling
- environment-based security configuration validation
- structured logging formatter output
- async database session setup via reusable engine and test fixtures

## Run linting

```bash
ruff check .
ruff format .
```

## How to extend this template

When you add a new feature, try to keep the same layering used by the existing auth flow:

1. Define or update the database model in `app/db/models` if the feature needs persistent data.
2. Create or update request and response schemas in `app/schemas` so validation and OpenAPI docs stay accurate.
3. Implement business logic in `app/services` instead of putting database or domain logic directly in route handlers.
4. Add the HTTP endpoints in `app/api/v1/endpoints` and keep them focused on request parsing, dependency injection, and response shaping.
5. Register the new router in `app/api/v1/router.py` so the endpoints are exposed under `/api/v1`.
6. Add or update tests in `tests/` for success cases, validation failures, auth behavior, and permission checks.
7. Create a new Alembic migration whenever the schema changes.

Use each folder for one clear responsibility:

- `app/db/models`: SQLAlchemy ORM models that represent database tables.
- `app/schemas`: Pydantic models for request validation, response serialization, and Swagger examples.
- `app/services`: reusable business logic, data access coordination, and feature workflows.
- `app/api/v1/endpoints`: route handlers for each resource or feature area.
- `app/api/dependencies`: shared dependencies such as authentication, current-user lookup, and role checks.

Recommended workflow for adding a new feature:

1. Start with the schema and data model.
2. Add the service-layer functions.
3. Expose the feature through an endpoint.
4. Add tests.
5. Update the docs and examples.

A practical example:

- If you want to add a `projects` feature, create `app/db/models/project.py` for the table definition.
- Add `app/schemas/project.py` for request and response contracts.
- Add `app/services/projects.py` for create/list/update business logic.
- Add `app/api/v1/endpoints/projects.py` for the API routes.
- Include the router in `app/api/v1/router.py`.
- Add tests such as `tests/api/v1/test_projects.py`.
- Generate a migration with `alembic revision --autogenerate -m "add projects table"` and apply it with `alembic upgrade head`.

A few rules help keep the template maintainable:

- Reuse shared auth dependencies from `app/api/dependencies` instead of re-implementing token parsing or role checks in each endpoint.
- Keep application code async and continue using `AsyncSession` dependencies for database access.
- Prefer environment variables for security-sensitive configuration such as database URLs, JWT secrets, and admin bootstrap credentials.
- Keep sample request and response examples updated whenever endpoint contracts change so the Swagger documentation remains helpful.
- Avoid putting business logic directly in route handlers; if an endpoint starts doing too much, move that logic into a service.
