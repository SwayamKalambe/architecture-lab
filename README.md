# Architecture Lab

Architecture Lab is a backend project for exploring and comparing **monolithic and microservices architectures** using an e-commerce system.

The current implementation is a modular **FastAPI monolith** using PostgreSQL, SQLAlchemy, and Alembic.

## Tech Stack

* Python 3.10+
* FastAPI
* SQLAlchemy
* PostgreSQL
* Pydantic
* Alembic
* Uvicorn

## Project Structure

```text
.
├── main.py
├── core/
│   ├── database.py
│   └── create_tables.py
├── monolith/
│   ├── users/
│   ├── products/
│   ├── carts/
│   └── orders/
├── alembic/
├── alembic.ini
├── requirements.txt
└── .env
```

The application is organized by business domain to keep the monolith modular.

## Current Features

* Create and retrieve users
* Create and retrieve products
* Add products to a user's cart
* PostgreSQL database integration with SQLAlchemy
* Pydantic request validation
* Alembic database migrations
* Interactive API documentation with Swagger and ReDoc

The `orders` package currently contains models and schemas but is not registered with the API.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install uvicorn
```

Create a `.env` file:

```env
DATABASE_URL=postgresql://username:password@localhost/architecture_lab
```

Initialize the database:

```bash
python -m core.create_tables
```

Or apply Alembic migrations:

```bash
alembic upgrade head
```

## Run

```bash
python -m uvicorn main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```
