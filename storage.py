import sqlite3

DB_File = 'tasks.db'


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_File)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_task(row: sqlite3.Row) -> dict:
    return {'id': row['id'], 'title': row['title'], 'done': bool(row['done'])}


def init_db() -> None:
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id    INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done  BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    count = cur.execute('select count(*) from tasks').fetchone()[0]
    if count == 0:
        cur.executemany(
            "insert into tasks (title, done) values (?, ?)",
            [
                ("Make Notes", 0),
                ("Prepare Quiz", 0),
                ("Complete Assignment", 1),
            ],
        )
    conn.commit()
    conn.close()


def list_tasks() -> list[dict]:
    conn = get_db()
    rows = conn.execute('select * from tasks order by id').fetchall()
    conn.close()
    return [row_to_task(row) for row in rows]


def get_task(task_id: int) -> dict | None:
    conn = get_db()
    row = conn.execute("select * from tasks where id = ?", (task_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return row_to_task(row)


def create_task(title: str, done: bool = False) -> dict:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, done),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, "title": title, "done": done}


def update_task(task_id: int, title: str | None, done: bool | None) -> dict | None:
    conn = get_db()
    row = conn.execute("select * from tasks where id = ?", (task_id,)).fetchone()
    if row is None:
        conn.close()
        return None
    new_title = row['title'] if title is None else title
    new_done = row['done'] if done is None else done
    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (new_title, new_done, task_id),
    )
    conn.commit()
    conn.close()
    return {"id": task_id, "title": new_title, "done": bool(new_done)}


def delete_task(task_id: int) -> bool:
    conn = get_db()
    cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    return deleted