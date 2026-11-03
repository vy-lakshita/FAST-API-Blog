# FAST-API-Blog

A simple blog website built with Python and FastAPI. Posts and users are saved in a database. The stored blogs can be read by anyone visiting the website.

## Features

- Posts and users are stored in a SQLite database (`blog.db`), created automatically on first run.
- The website shows all posts, a single post, and each user's posts.
- The API supports create, read, update and delete (CRUD) for users and posts.
- Pydantic schemas validate input data, and SQLAlchemy models define the database tables.
- Error handling using  friendly error page for the website.

## Project Structure

| File / Folder | Purpose |
|---|---|
| `main.py` | Routes |
| `database.py` | Database connection |
| `models.py` | Database tables |
| `schemas.py` | Data validation |
| `templates/` | HTML pages |
| `static/` and `media/` | CSS, icons and profile pictures |
