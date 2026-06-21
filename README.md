# Team SaaS

Team SaaS is a small FastAPI backend for managing users, organizations, and projects.

It includes:

- user registration and login with JWT access tokens
- organization creation
- project creation and listing scoped to a user's organization
- SQLAlchemy models with Alembic migrations
- a basic test suite for the auth and project flow

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL-compatible database URL
- Pydantic Settings
- Passlib and python-jose for password hashing and JWT auth
- Pytest for tests

## Project Structure

- `app/main.py` - FastAPI app entrypoint
- `app/core/` - settings and auth helpers
- `app/db/` - database engine and session setup
- `app/models/` - SQLAlchemy models
- `app/schemas/` - Pydantic request/response schemas
- `app/api/routes/` - API routers
- `alembic/` - database migrations
- `tests/` - integration-style API tests

## API Summary

- `POST /auth/register` - create a user
- `POST /auth/login` - return a bearer token
- `GET /auth/me` - fetch the current user
- `POST /organizations/` - create an organization and attach it to the logged-in user
- `POST /projects/` - create a project in the current user's organization
- `GET /projects/` - list projects in the current user's organization

## Fresh Clone Setup

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

The app reads configuration from `.env` via `app/core/config.py`.

Set these variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/team_saas
SECRET_KEY=change-me-to-a-long-random-string
ALGORITHM=HS256
```

Notes:

- `DATABASE_URL` must point to a database you can reach from your machine.
- The repo uses `psycopg2-binary`, so a PostgreSQL URL is the expected setup.
- `SECRET_KEY` should be unique per environment.

### 4. Run database migrations

Once the database exists and `.env` is set, apply the schema:

```bash
alembic upgrade head
```

This repo currently has these migrations:

- initial tables
- a follow-up migration that makes user email and password required

### 5. Start the API server

```bash
uvicorn app.main:app --reload
```

The server will usually be available at:

- `http://127.0.0.1:8000`

Interactive API docs are available at:

- `http://127.0.0.1:8000/docs`

## Running Tests

```bash
pytest
```

The test suite currently covers:

- register/login flow
- organization creation
- project creation and organization-scoped project listing

## How Authentication Works

- `POST /auth/login` returns a JWT access token.
- Send the token in the `Authorization` header:

```bash
Authorization: Bearer <token>
```

- Protected endpoints use that token to identify the current user.

## Data Model

- `User`
  - unique email
  - password hash
  - optional `organization_id`
- `Organization`
  - unique name
- `Project`
  - name
  - optional `organization_id`

## Common Issues

- If the app fails at startup, check that `.env` exists and that `DATABASE_URL`, `SECRET_KEY`, and `ALGORITHM` are set.
- If migrations fail, verify the database exists and is reachable.
- If auth fails, make sure you are sending the bearer token in the `Authorization` header.

