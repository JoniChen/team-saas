# Team SaaS

![CI](https://github.com/JoniChen/team-saas/actions/workflows/ci.yml/badge.svg)

Team SaaS is a FastAPI backend for managing users, organizations, and projects with JWT authentication and PostgreSQL.

It includes:

- User registration and login with JWT access tokens
- Organization creation and membership
- Project creation and listing scoped to a user's organization
- SQLAlchemy models with Alembic migrations
- Structured JSON logging with per-request IDs
- Health and readiness endpoints
- Integration test suite

## Tech Stack

- FastAPI + Uvicorn
- SQLAlchemy 2.0 + Alembic
- PostgreSQL
- Pydantic v2 + Pydantic Settings
- Passlib (bcrypt) + python-jose (JWT)
- Pytest + pytest-cov
- Ruff (lint + format) + Mypy (type checking)

## Project Structure

```
app/
  main.py           — FastAPI app, middleware, health endpoints
  core/             — settings, security, logging
  db/               — engine and session
  models/           — SQLAlchemy models (User, Organization, Project)
  schemas/          — Pydantic request/response schemas
  api/routes/       — API routers
alembic/            — database migrations
tests/              — integration tests
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /auth/register | — | Create a user |
| POST | /auth/login | — | Return a bearer token |
| GET | /auth/me | required | Fetch the current user |
| POST | /organizations/ | required | Create an org and assign the current user |
| POST | /projects/ | required | Create a project in the user's org |
| GET | /projects/ | required | List projects in the user's org |
| GET | /health | — | Liveness check |
| GET | /health/ready | — | Readiness check (verifies DB connectivity) |

## Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

For running the app:

```bash
pip install -r requirements.txt
```

For development (adds ruff, mypy, pytest-cov, pre-commit):

```bash
pip install -r requirements-dev.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql://user:password@localhost:5432/team_saas
SECRET_KEY=change-me-to-a-long-random-string
ALGORITHM=HS256
```

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

## Running Tests

```bash
pytest
```

With coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

## Code Quality

```bash
ruff check .       # lint
ruff format .      # format
mypy app/          # type check
```

To enable pre-commit hooks (runs ruff on every commit):

```bash
pre-commit install
```

## Authentication

`POST /auth/login` returns a JWT bearer token. Pass it on subsequent requests:

```
Authorization: Bearer <token>
```

## Data Model

- **User** — email, password hash, optional `organization_id`, timestamps
- **Organization** — unique name, timestamps
- **Project** — name, `organization_id` (scoped to one org), timestamps

All primary keys and foreign keys are native PostgreSQL `UUID` types.

## Common Issues

- If startup fails, check that `.env` exists with `DATABASE_URL`, `SECRET_KEY`, and `ALGORITHM` set.
- If migrations fail, verify the database exists and is reachable.
- If auth fails, confirm the `Authorization: Bearer <token>` header is present.
