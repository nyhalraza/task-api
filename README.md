# Task API v1 - Simple CRUD FastAPI

A simple CRUD API for managing a to-do list, built with FastAPI. Supports creating, reading, updating, and deleting tasks, with interactive Swagger UI docs.

## What this is

This API lets you manage a list of tasks. Each task has:
- `id` (number) — assigned automatically by the server
- `title` (text) — required
- `done` (true/false) — defaults to `false`

## How to install & run it

**Requirements:** Python 3.8+

```bash
pip install -r requirements.txt
uvicorn myapi:app --reload
```

The server runs at `http://localhost:8000`.

Interactive docs (Swagger UI) are available at `http://localhost:8000/docs`.

## Endpoints

| Method | Path              | Description                              |
|--------|-------------------|-------------------------------------------|
| GET    | `/`                | API info (name, version, endpoints)       |
| GET    | `/health`          | Health check — returns `{"status": "ok"}` |
| GET    | `/tasks`           | List all tasks                            |
| GET    | `/tasks/{id}`      | Get a single task by ID                   |
| POST   | `/tasks`           | Create a new task                         |
| PUT    | `/tasks/{id}`      | Update a task's `title` and/or `done`     |
| DELETE | `/tasks/{id}`      | Delete a task                             |

## Example request

```bash
curl.exe -i http://localhost:8000/tasks
```

```
HTTP/1.1 200 OK
date: Sat, 29 Aug 2026 12:26:35 GMT
server: uvicorn
content-length: 131
content-type: application/json
```

## Swagger UI

![Swagger UI screenshot](./swagger-screenshot.png)

## Notes

- Data is stored in memory — restarting the server resets tasks back to the 3 seeded examples.
- Status codes follow REST conventions: `201` on create, `200` on successful read/update, `204` on successful delete, `404` for missing tasks, `400`/`422` for invalid input.


# Task API v2 — FastAPI + SQLite

## Why SQLite?
SQLite stores the entire database in a single local file (`tasks.db`) with no
server to install or configure. It is perfect for development, learning, and
small apps, and the Python standard library ships with the `sqlite3` module,
so there are no extra dependencies.

## Where the data lives
The database file `tasks.db` is created automatically in the project root the
first time the app runs. Delete the file to start completely fresh.

## How to run
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```
The `tasks` table is created (and seeded with 3 example tasks, only once) at startup.

## Manual SQL exploration (Stage 4)
Open `tasks.db` in DB Browser for SQLite and try:
```sql
SELECT * FROM tasks;
SELECT * FROM tasks WHERE done = 1;
SELECT COUNT(*) FROM tasks;
UPDATE tasks SET done = 1;
DELETE FROM tasks WHERE done = 1;
```
Changes made directly in the database show up immediately in the API.
