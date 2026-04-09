# Project Rules

This repository is a reusable, production-ready FastAPI template. Every change should preserve that goal.

The template should stay:

- generic enough for multiple API projects
- production-minded in structure and defaults
- easy for another developer to understand quickly
- consistent in naming, layering, and documentation

## Core principles

- Prefer clarity over cleverness.
- Prefer explicit structure over hidden behavior.
- Prefer small, composable modules over large catch-all files.
- Prefer predictable conventions over one-off patterns.
- Prefer code that helps the next developer move faster.

## Architectural boundaries

Each top-level package inside `app/` has a clear responsibility:

- `app/api`: HTTP-facing routing, API versioning, endpoint registration, and shared API dependencies
- `app/core`: cross-cutting application concerns such as config, security, exceptions, error handlers, and logging
- `app/db`: database setup, SQLAlchemy base/session, and ORM models
- `app/schemas`: Pydantic models for request validation, response serialization, and OpenAPI examples
- `app/services`: business logic and feature workflows
- `app/scripts`: explicit operational scripts such as one-time bootstrap tasks

Do not blur these boundaries without a strong reason.

Examples:

- Validation models belong in `app/schemas`, not in route files.
- Database tables belong in `app/db/models`, not in `app/schemas`.
- Business logic belongs in `app/services`, not in endpoints.
- Logging configuration belongs in `app/core/logging`, not in random feature modules.

## API design rules

### Route naming

- Use resource-oriented names where possible.
- Avoid vague action-heavy names unless the action is the real resource.
- Keep route names stable and easy to understand from the URL alone.

Good examples:

- `POST /api/v1/users`
- `POST /api/v1/auth/tokens`
- `GET /api/v1/users/current`
- `GET /api/v1/admin/overview`

### Endpoint structure

Each endpoint should:

- declare a clear `summary`
- include a useful `description`
- use request and response schemas where appropriate
- document important error responses
- keep handler logic thin

Endpoints should mostly do this:

1. receive validated input
2. call dependencies
3. delegate business logic to services
4. return serialized response models

Endpoints should not:

- contain complex branching business rules
- manually duplicate auth logic
- directly manage low-level DB concerns when a service should own them

### API versioning

- Keep versioned endpoints under `app/api/v1`.
- New route groups should be registered in `app/api/v1/router.py`.
- Avoid mixing unversioned routes into the main router unless there is a strong platform-level reason.

## Schema rules

Schemas in `app/schemas` are the contract between the API and its clients.

They should:

- validate request data
- shape response data
- provide field descriptions
- include examples when the endpoint is public or reusable

When updating a schema:

- update the tests that depend on it
- update any endpoint descriptions if the behavior changes
- update README examples when the change is user-facing

Do not use ORM models as API response models directly.

## Database rules

### Models

- Keep ORM models in `app/db/models`.
- Use explicit field names and types.
- Keep models generic unless the template is intentionally being extended for a specific domain.

### Session usage

- Use `AsyncSession` for application database access.
- Use the shared DB dependency from `app/db/session.py`.
- Do not introduce synchronous DB code into request handlers unless there is a very strong reason and the repo is explicitly being redesigned for it.

### Migrations

- Every schema change must include an Alembic migration.
- Model changes and migration files should usually be committed together.
- Do not rely on application startup to create or mutate the schema.
- Treat Alembic revisions as part of the source of truth.

Expected migration workflow:

1. update the model
2. create a migration
3. review the generated migration
4. apply the migration locally
5. commit both the model and migration

## Service layer rules

Services in `app/services` should contain reusable business logic.

Services are a good place for:

- orchestration across multiple repositories or models
- business validation beyond request schema validation
- persistence workflows
- auth-related workflows
- bootstrap logic used by scripts

Services should not:

- return raw FastAPI responses
- know about request objects
- format HTTP exceptions directly when a domain exception is more appropriate

## Error handling rules

The template uses domain exceptions plus centralized global handlers.

Rules:

- Prefer custom domain exceptions from `app/core/exceptions` over scattering `HTTPException` everywhere.
- Keep response formatting centralized in `app/core/error_handlers.py`.
- Keep the shared error response envelope stable unless intentionally making a breaking change.
- Preserve request IDs in error responses.

When introducing a new exception:

1. define it in the correct exception module
2. keep the status, code, and message explicit
3. let the global handler translate it
4. add tests covering the behavior

## Logging rules

Logging should remain structured and production-friendly.

Current logging split:

- `app/core/logging/config.py`: logging configuration
- `app/core/logging/formatters.py`: JSON formatter
- `app/core/logging/middleware.py`: request logging middleware

Rules:

- Keep request logs machine-readable by default.
- Keep log configuration centralized.
- Preserve request IDs in both logs and responses.
- Do not log secrets, raw passwords, or sensitive tokens.
- Use environment-aware log levels.

If you add new logging behavior, make sure it improves observability without leaking sensitive information.

## Security rules

- Never hardcode real secrets in source code.
- Use environment variables for database URLs, JWT secrets, and environment-specific credentials.
- Commit `.env.example`, not `.env`.
- Keep password validation strong by default.
- Preserve or improve auth, token, and role-check flows.
- Avoid weakening defaults just to make local setup easier.

If a new feature introduces a secret or sensitive config value:

1. add it to config
2. add it to `.env.example`
3. document it in `README.md`
4. avoid embedding real values in code or docs

## Middleware rules

Middleware should remain explicit and focused.

Good middleware concerns:

- request logging
- request ID propagation
- timing
- security headers

Avoid middleware that hides feature-specific business behavior.

## Testing rules

Testing is part of the template contract.

Rules:

- Add or update tests for meaningful behavior changes.
- Keep the default suite passing.
- Maintain the configured coverage threshold.
- Prefer tests that cover:
  - happy paths
  - validation failures
  - authentication failures
  - authorization failures
  - standardized error responses
  - config validation
  - logging helpers when they change

When changing APIs:

- update API tests
- update schema examples if needed
- update docs when behavior changes

When changing config/security:

- add tests for invalid and valid config combinations

## Documentation rules

Documentation should stay aligned with the code.

Update `README.md` when you change:

- setup instructions
- environment variables
- API routes
- auth flow
- migration workflow
- testing commands
- extension guidance
- project structure

Examples in docs should remain realistic, generic, and consistent with the current API.

## Naming rules

- Use descriptive, boring names over clever names.
- Prefer `users.py`, `auth.py`, `projects.py` over vague names like `helpers.py` or `manager.py`.
- Avoid broad dump folders such as `shared` unless there is a very clear definition for what belongs there.

## Folder creation rules

Before adding a new folder, ask:

1. does this concern already have a home?
2. will multiple files actually live here?
3. does the new folder make the project clearer, not just more complex?

Good reasons to add a folder:

- multiple modules in a concern are growing
- a concern already exists conceptually and needs clearer separation
- the new structure improves discoverability

Bad reasons:

- copying another repo blindly
- making the tree look “enterprise”
- moving one file into a folder without a real benefit

## Change management rules

- Prefer focused changes over broad rewrites.
- Preserve working patterns unless there is a clear benefit to changing them.
- Avoid introducing unnecessary abstraction layers like facades, repositories, or generic utilities without real need.
- Keep the template reusable; avoid baking in feature-specific assumptions unless the exercise explicitly requires them.

## Final checklist for contributors

Before considering a change complete, check:

- Does the code fit the existing structure?
- Are tests updated and passing?
- Does coverage still pass?
- Are docs updated if behavior changed?
- Are secrets/config handled safely?
- Is the change still appropriate for a reusable template?
