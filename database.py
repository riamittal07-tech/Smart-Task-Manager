import sqlite3

connection = sqlite3.connect("tasks.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    task TEXT,
    priority TEXT,
    category TEXT,
    due_date TEXT,
    completed INTEGER

)
""")

connection.commit()
connection.close()


def connect_db():
    connection = sqlite3.connect("tasks.db")
    return connection


def add_task(task, priority, category, due_date, completed):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO tasks
    (task, priority, category, due_date, completed)

    VALUES (?, ?, ?, ?, ?)
    """,
    (task, priority, category, due_date, completed)
    )

    connection.commit()

    connection.close()

def get_tasks():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM tasks")

    tasks = cursor.fetchall()

    connection.close()

    return tasks

def update_task(old_task, new_task):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET task = ?
        WHERE task = ?
        """,
        (new_task, old_task)
    )

    connection.commit()

    connection.close()

def delete_task(task_name):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE task = ?
        """,
        (task_name,)
    )

    connection.commit()

    connection.close()
def update_completed(task_name, completed):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE tasks
        SET completed = ?
        WHERE task = ?
        """,
        (completed, task_name)
    )

    connection.commit()

    connection.close()