# Users CRUD API

A small back end for creating, reading, updating and deleting users, built with FastAPI, SQLAlchemy and SQLite.

## Stack

- FastAPI — routing and request/response handling
- SQLAlchemy — ORM and database layer
- SQLite — local file-based database
- Pydantic — request and response validation
- Uvicorn — ASGI development server

## Endpoints

| Method | Path            | Description        |
|--------|-----------------|---------------------|
| POST   | /users/         | Create a user       |
| GET    | /users/         | List all users      |
| GET    | /users/{id}     | Get a single user    |
| PUT    | /users/{id}     | Update a user        |
| DELETE | /users/{id}     | Delete a user        |

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs available at `http://127.0.0.1:8000/docs`.

## Project structure

```
app/
├── __init__.py
├── main.py        # app instance and routes
├── database.py     # engine, session, get_db dependency
├── models.py        # SQLAlchemy models
└── schemas.py        # Pydantic schemas
```
