# Bookly FastAPI Project

Bookly is a RESTful API for managing books, built with FastAPI, SQLModel, and async SQLAlchemy. It supports CRUD operations for books and is designed for asynchronous, production-ready use.

## Features

- **Async CRUD**: Create, read, update, and delete books asynchronously.
- **SQLModel & SQLAlchemy**: Modern ORM with async support.
- **Pydantic Schemas**: Data validation and serialization.
- **Modular Structure**: Organized by routers, services, and schemas.
- **Error Handling**: Consistent HTTP error responses.

## Project Structure

```
Bookly/
│
├── db/
│   └── main.py           # Database engine and session management
├── src/
│   └── books/
│       ├── books.py      # Book API routes
│       └── services.py   # Business logic for books
├── models/
│   └── models.py         # SQLModel ORM models
├── schemas/
│   └── schemas.py        # Pydantic schemas for request/response
├── config/
│   └── config.py         # Configuration (e.g., database URL)
├── main.py               # FastAPI app entrypoint
└── README.md
```

## Setup

1. **Clone the repository**
    ```sh
    git clone https://github.com/yourusername/bookly.git
    cd bookly
    ```

2. **Create and activate a virtual environment**
    ```sh
    python -m venv venv
    venv\Scripts\activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Configure environment**
    - Edit `config/config.py` and set your `DATABASE_URL` (use an async driver, e.g., `postgresql+asyncpg://...`).

5. **Run database migrations**
    ```sh
    # If using Alembic or similar, otherwise tables auto-create on startup
    ```

6. **Start the server**
    ```sh
    uvicorn main:app --reload
    ```

7. **Access the API docs**
    - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser.

## Example Endpoints

- `GET /books/` — List all books
- `POST /books/` — Create a new book
- `GET /books/{book_uid}` — Get a book by ID
- `PATCH /books/{book_uid}` — Update a book
- `DELETE /books/{book_uid}` — Delete a book

## License

MIT License

---

**Happy coding!**