# FastAPI Template

A reusable, production-minded FastAPI boilerplate that gives teams a clean starting point for API projects. This version includes JWT authentication, role-based access control, SQLite-backed persistence, versioned routing, strong request validation, and a practical test suite that other developers can extend safely.

## Features

- FastAPI application factory-style setup in a simple, modular layout
- JWT authentication with secure password hashing using Argon2 via `pwdlib`
- User registration and login with bearer token protection
- Role-based access control with `user` and `admin` examples
- SQLAlchemy-based persistence with SQLite as the default local database
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
4. Update secrets and admin credentials for your environment.
5. Run the app.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env
uvicorn app.main:app --reload
```

Open the following URLs after startup:

- App: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/api/v1/health`

## Database migrations

Alembic is included so schema changes are tracked instead of relying only on `create_all()`.

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

For local development, the app still creates missing tables at startup to keep the template easy to run. Alembic should be the source of truth for evolving schemas across environments.

## Environment variables

All application settings are namespaced with `APP_` to avoid collisions with machine-level variables.

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_NAME` | Human-readable API name | `FastAPI Template` |
| `APP_ENV` | Environment label for responses and config | `local` |
| `APP_DEBUG` | FastAPI debug mode | `false` |
| `APP_API_V1_PREFIX` | Prefix for version 1 routes | `/api/v1` |
| `APP_VERSION` | API version shown in docs | `0.1.0` |
| `APP_DATABASE_URL` | SQLAlchemy database URL | `sqlite:///./fastapi_template.db` |
| `APP_SECRET_KEY` | JWT signing secret | `change-me-with-a-long-random-secret` |
| `APP_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes | `30` |
| `APP_DEFAULT_ADMIN_EMAIL` | Seeded admin account email | `admin@example.com` |
| `APP_DEFAULT_ADMIN_PASSWORD` | Seeded admin account password | `ChangeMe123!` |

Change `APP_SECRET_KEY` and the default admin credentials before any non-local deployment.

## Authentication flow

### Register

`POST /api/v1/auth/register`

```json
{
  "email": "developer@example.com",
  "password": "StrongPassword123!"
}
```

### Login

`POST /api/v1/auth/login`

```json
{
  "email": "developer@example.com",
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

## Protected routes

- `GET /api/v1/users/me`: any authenticated user
- `GET /api/v1/admin/summary`: admin role only

The template seeds a default admin account on startup using `APP_DEFAULT_ADMIN_EMAIL` and `APP_DEFAULT_ADMIN_PASSWORD`.

## Run tests

```bash
pytest
```

The tests cover:

- health endpoint availability
- user registration
- successful login
- protected route access
- role-based access control
- invalid credential handling

## Run linting

```bash
ruff check .
ruff format .
```

## How to extend this template

- Add new business logic in `app/services`
- Add request and response contracts in `app/schemas`
- Add new database models in `app/db/models`
- Add new route groups in `app/api/v1/endpoints`
- Reuse shared auth dependencies from `app/api/dependencies`
- Replace SQLite with PostgreSQL by changing `APP_DATABASE_URL`
- Add new Alembic revisions in `alembic/versions` when the schema changes

## Suggested next improvements

- refresh token support
- account verification and password reset flows
- migration support with Alembic
- structured logging and request correlation IDs
- CORS and trusted host middleware
- Docker and CI pipeline setup
