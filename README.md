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
- environment-based secret validation so placeholder secrets are rejected outside local and test environments

Password rules for account creation:

- at least 8 characters
- at least one uppercase letter
- at least one lowercase letter
- at least one number
- at least one special character

## Environment variables

All application settings are namespaced with `APP_` to avoid collisions with machine-level variables.

| Variable | Purpose | Default |
| --- | --- | --- |
| `APP_NAME` | Human-readable API name | `FastAPI Template` |
| `APP_ENV` | Environment label for responses and config | `local` |
| `APP_DEBUG` | FastAPI debug mode | `false` |
| `APP_API_V1_PREFIX` | Prefix for version 1 routes | `/api/v1` |
| `APP_VERSION` | API version shown in docs | `0.1.0` |
| `APP_DATABASE_URL` | Async SQLAlchemy database URL | `postgresql+asyncpg://postgres:postgres@localhost:5432/fastapi_template` |
| `APP_DB_POOL_SIZE` | Base PostgreSQL connection pool size | `10` |
| `APP_DB_MAX_OVERFLOW` | Extra pooled connections allowed above the base pool | `20` |
| `APP_DB_POOL_TIMEOUT` | Seconds to wait for a pooled connection | `30` |
| `APP_DB_POOL_RECYCLE` | Seconds before recycling a pooled PostgreSQL connection | `1800` |
| `APP_SECRET_KEY` | JWT signing secret | `change-me-with-a-long-random-secret` |
| `APP_ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime in minutes | `30` |
| `APP_CORS_ALLOW_ORIGINS` | Comma-separated allowed origins for browser clients | `http://localhost:3000,http://127.0.0.1:3000` |
| `APP_CORS_ALLOW_CREDENTIALS` | Whether browsers may send credentials on cross-origin requests | `true` |
| `APP_CORS_ALLOW_METHODS` | Comma-separated HTTP methods exposed by CORS | `GET,POST,PUT,PATCH,DELETE,OPTIONS` |
| `APP_CORS_ALLOW_HEADERS` | Comma-separated allowed request headers for CORS | `Authorization,Content-Type` |
| `APP_DEFAULT_ADMIN_EMAIL` | Seeded admin account email | `aditi.admin@example.com` |
| `APP_DEFAULT_ADMIN_PASSWORD` | Seeded admin account password | `ChangeMe123!` |

Change `APP_SECRET_KEY` and the default admin credentials before any non-local deployment. The app rejects the placeholder secret key and admin password outside `local` and `test` environments.

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
- password strength validation
- email format validation
- CORS preflight behavior
- protected route access
- role-based access control
- invalid credential handling
- environment-based security configuration validation
- async database session setup via reusable engine and test fixtures

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
- Keep async application code on `AsyncSession` dependencies
- Add new Alembic revisions in `alembic/versions` when the schema changes
- Prefer environment variables for security-sensitive configuration
- Update request and response examples whenever endpoint contracts change

## Suggested next improvements

- refresh token support
- account verification and password reset flows
- structured logging and request correlation IDs
- CORS and trusted host middleware
- Docker and CI pipeline setup
