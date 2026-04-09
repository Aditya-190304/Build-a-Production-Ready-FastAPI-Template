# Agent Instructions

This document is for AI coding assistants, automated contributors, and agentic tools working in this repository.

Your job is not just to make the code work. Your job is to keep the repository usable as a reusable, production-ready FastAPI template for the next developer.

## Primary objective

Preserve and improve the repository as a generic FastAPI starter that demonstrates:

- clean modular structure
- authentication and authorization patterns
- secure configuration handling
- async database usage
- Alembic migrations
- standardized error handling
- structured logging
- useful testing and documentation

Do not optimize for novelty. Optimize for consistency, safety, and maintainability.

## How to think about this repo

This is a template repository, not a domain-specific product.

That means:

- keep examples generic
- avoid business-specific assumptions unless explicitly requested
- prefer patterns that other developers can copy into future projects
- use Indian example names only where examples are helpful and already consistent with the repo

## Repository map

Use the current structure as the source of truth:

- `app/api/v1/endpoints`: HTTP route handlers
- `app/api/dependencies`: shared auth and request dependencies
- `app/services`: business logic and reusable workflows
- `app/schemas`: request/response validation and API contract models
- `app/db/models`: SQLAlchemy ORM models
- `app/db`: database base, engine, and session management
- `app/core/config.py`: environment-based settings
- `app/core/security.py`: hashing, token creation, token decoding
- `app/core/exceptions`: custom domain exceptions
- `app/core/error_handlers.py`: global exception handling
- `app/core/logging`: logging config, formatter, and middleware
- `app/scripts`: explicit operational scripts
- `tests`: API, logging, and config tests

## Behavioral expectations

### 1. Respect architectural boundaries

When changing code:

- keep route handlers thin
- keep business logic in services
- keep request/response contracts in schemas
- keep ORM models in `app/db/models`
- keep config/security/exceptions/logging in `app/core`

If you are unsure where code belongs, prefer the existing pattern already used by the auth flow.

### 2. Prefer extension over invention

When adding a feature:

- follow the same structure already used in the repo
- reuse existing helpers and patterns
- avoid inventing a second competing pattern unless the task explicitly requires a redesign

Examples:

- use `AsyncSession`, do not introduce sync DB access casually
- use the centralized error system, do not create per-endpoint response formatting
- use the logging package, do not configure logging ad hoc in feature modules

### 3. Keep the repo template-friendly

Avoid changes that make the repo less reusable, such as:

- adding app-specific business language everywhere
- hardcoding real secrets
- assuming Docker exists when it does not
- adding unnecessary layers just because another stack uses them
- leaving stale docs after code changes

## API change instructions

When you add or change an endpoint:

1. update or create the endpoint in `app/api/v1/endpoints`
2. ensure the route has a clear `summary`
3. ensure the route has a useful `description`
4. use request/response schemas from `app/schemas`
5. add or update response examples where helpful
6. document important error responses
7. add or update tests
8. update the README if the public API or workflow changed

Good route behavior:

- accept validated input
- delegate to services
- return response models
- rely on shared dependencies for auth/authorization
- raise domain exceptions where appropriate

Avoid:

- embedding large business rules in endpoints
- direct manual response formatting for reusable error cases
- duplicate auth logic

## Database change instructions

When changing the database layer:

1. update the model in `app/db/models`
2. generate an Alembic migration
3. review the generated revision
4. apply the migration locally
5. update tests if behavior changed
6. update README if the workflow or setup changed

Never assume startup should mutate the schema.

Do not:

- reintroduce `create_all()` as the main runtime schema strategy
- make schema changes without a migration
- mix ORM models and API schemas

## Error handling instructions

This repo intentionally uses a domain-exception pattern.

Expected flow:

1. services or dependencies raise custom exceptions
2. `app/core/error_handlers.py` catches them globally
3. the handler returns the standardized error envelope

When introducing a new exception:

- place it in the appropriate module under `app/core/exceptions`
- give it an explicit status code, code, and message
- keep naming specific and descriptive
- add tests for the resulting API behavior

Do not:

- scatter repetitive `HTTPException` creation everywhere when a domain exception is the better fit
- break the shared error envelope without updating the docs and tests

## Logging instructions

The logging package is intentionally split by responsibility:

- `config.py`: setup
- `formatters.py`: output structure
- `middleware.py`: request lifecycle logging

When changing logging:

- keep structured JSON as the default unless explicitly asked otherwise
- preserve request IDs
- avoid logging secrets or raw sensitive data
- keep environment-aware log levels intact
- add or update tests if formatter or behavior changes

If you need new logging fields, make sure they are:

- useful for debugging or observability
- safe to emit
- consistent across requests

## Config and security instructions

When adding a new setting:

1. add it to `app/core/config.py`
2. add it to `.env.example` if developers need to set it
3. document it in `README.md`
4. add validation if misuse would be risky
5. add tests if the setting affects behavior or safety

Never:

- hardcode real secrets
- commit `.env`
- bypass security validation just to simplify a local example

## Testing instructions

Every meaningful code change should be validated by tests.

Expected test behavior:

- `pytest` should pass
- coverage threshold should pass
- tests should be focused on behavior, not implementation trivia

When adding a feature, consider tests for:

- valid behavior
- invalid input
- permission failures
- standardized error responses
- config validation when relevant

If you change logs, exceptions, or config, update the relevant non-API tests too.

## Documentation instructions

You are responsible for keeping documentation in sync with the code.

Update `README.md` when you change:

- setup commands
- environment variables
- route names
- auth flow
- migrations
- testing instructions
- coverage behavior
- project structure
- extension guidance

When editing documentation:

- prefer concrete commands over vague language
- prefer current repo structure over generic advice
- keep examples aligned with actual code

## Decision rules for new structure

Before creating a new file or folder, ask:

1. does this concern already have a clear home?
2. is the current module actually getting too large?
3. will the new location make the repo easier to navigate?

Good structural changes:

- splitting a growing concern by responsibility
- creating a small package for a real cross-cutting concern
- improving discoverability

Bad structural changes:

- adding layers without active need
- creating vague dump folders
- copying another repo’s structure without adapting it

## Preferred style when editing code

- use descriptive names
- preserve async patterns
- keep functions focused
- keep examples/docs accurate
- keep imports organized
- follow the repo’s current conventions before introducing new ones

## Preferred style when making tradeoffs

If there is a conflict, prefer this order:

1. correctness
2. security
3. maintainability
4. consistency with repo structure
5. developer convenience
6. minimalism

## Agent completion checklist

Before finishing work, verify:

- code fits the architecture
- tests pass
- coverage still passes
- lint passes
- docs are updated if needed
- `.env.example` is updated if settings changed
- no real secrets were added
- the repo is still a reusable template, not a one-off app
