# GEMINI.md - Project Context

## Project Overview
`restaurant_api` is a RESTful API built with **FastAPI** designed for managing restaurant operations, including users, bookings, delivery, menu, and tables. It follows a modular architecture and uses **SQLAlchemy** (async) for database interactions and **Alembic** for migrations.

## Tech Stack
- **Framework:** FastAPI
- **Database ORM:** SQLAlchemy (Async)
- **Database Driver:** asyncpg
- **Migrations:** Alembic
- **Validation & Settings:** Pydantic
- **Security:** argon2-cffi, python-jose (JWT)
- **Web Server:** Uvicorn

## Project Structure
The project is organized into functional modules within the `app/` directory:
- `app/bookings/`: Management of restaurant bookings.
- `app/delivery/`: Delivery tracking and management.
- `app/menu/`: Restaurant menu and dish management.
- `app/tables/`: Table availability and management.
- `app/users/`: User authentication and profile management.
- `app/dao/`: Generic Data Access Object (DAO) patterns.
- `app/migration/`: Alembic migration scripts.

### Module Structure
Each module (e.g., `app/users/`) typically contains:
- `models.py`: SQLAlchemy database models.
- `schemas.py`: Pydantic models for data validation and serialization.
- `router.py`: FastAPI routes and endpoint logic.
- `dao.py`: Data Access Objects for database operations, inheriting from `BaseDAO`.

## Building and Running

### Prerequisites
- Python 3.10+
- PostgreSQL database

### Installation
1.  **Clone the repository.**
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure environment variables:**
    Create a `.env` file in the root directory and populate it based on `app/config.py`:
    ```env
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=your_user
    DB_PASS=your_password
    DB_NAME=your_db_name
    DB_DRIVER=postgresql+asyncpg
    DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRES_MINUTES=30
    ```

### Running the Application
To start the FastAPI server with auto-reload:
```bash
uvicorn app.main:app --reload
```

### Database Migrations
- **Apply migrations:**
  ```bash
  alembic upgrade head
  ```
- **Create a new migration:**
  ```bash
  alembic revision --autogenerate -m "description"
  ```

## Development Conventions

- **DAO Pattern:** All database interactions should go through a DAO. Inherit from `app.dao.base.BaseDAO` for standard CRUD operations.
- **Async/Await:** Use async database drivers and ensure all I/O-bound operations (DB, external APIs) use `async/await`.
- **Modularization:** When adding new features, create a new directory in `app/` with the standard `models`, `schemas`, `router`, and `dao` files.
- **Validation:** Use Pydantic schemas for all request and response bodies.
- **Authentication:** Use the existing authentication logic in `app/users/` (JWT via cookies).
