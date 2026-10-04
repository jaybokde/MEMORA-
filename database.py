import sqlite3

DATABASE_NAME = "database.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            deadline TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            date TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_memory(user_id, content, category=None):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO memories (user_id, content, category)
        VALUES (?, ?, ?)
        """,
        (user_id, content, category)
    )

    connection.commit()
    connection.close()


def save_task(user_id, title, description=None, deadline=None):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO tasks (user_id, title, description, deadline)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, title, description, deadline)
    )

    connection.commit()
    connection.close()


def save_event(user_id, title, date=None, description=None):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO events (user_id, title, date, description)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, title, date, description)
    )

    connection.commit()
    connection.close()


def get_memories(user_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT * FROM memories
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_tasks(user_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT * FROM tasks
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_events(user_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT * FROM events
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


if __name__ == "__main__":
    initialize_database()
    print("MEMORA database initialized successfully!")