import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]


def get_db():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def list_tasks() -> list[dict]:
    with get_db() as conn:
        return conn.execute("SELECT * FROM tasks ORDER BY id").fetchall()


def get_task(task_id: int) -> dict | None:
    with get_db() as conn:
        return conn.execute("SELECT * FROM tasks WHERE id = %s", (task_id,)).fetchone()



def create_task(title: str, done: bool = False) -> dict:
    with get_db() as conn:
        return conn.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *", (title, done)).fetchone()



def update_task(task_id: int, title: str | None, done: bool | None) -> dict | None:
    with get_db() as conn:
        return conn.execute("UPDATE tasks SET title = COALESCE (%s, title), done = COALESCE (%s, done) WHERE id = %s RETURNING *", (title, done, task_id, )).fetchone()
        

def delete_task(task_id: int) -> bool:
    with get_db() as conn:
        cur = conn.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        return cur.rowcount > 0
         