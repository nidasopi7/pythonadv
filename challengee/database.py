import os
import sqlite3
from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH", "recipes.db")


@contextmanager
def get_db():
    connection = sqlite3.connect(DATABASE_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL COLLATE NOCASE UNIQUE,
                description TEXT DEFAULT ''
            )
        """)

        db.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                cooking_time INTEGER NOT NULL DEFAULT 30,
                category_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id)
                    REFERENCES categories(id)
                    ON DELETE RESTRICT
            )
        """)

        count = db.execute(
            "SELECT COUNT(*) FROM categories"
        ).fetchone()[0]

        if count == 0:
            db.executemany(
                """
                INSERT INTO categories (name, description)
                VALUES (?, ?)
                """,
                [
                    ("Breakfast", "Morning meals"),
                    ("Lunch", "Lunch and light meals"),
                    ("Dinner", "Main meals"),
                    ("Desserts", "Sweet treats")
                ]
            )

            category_ids = {
                row["name"]: row["id"]
                for row in db.execute(
                    "SELECT id, name FROM categories"
                ).fetchall()
            }

            sample_recipes = [
                (
                    "Fluffy Pancakes",
                    "1 cup flour, 1 egg, 3/4 cup milk, 1 tsp baking powder",
                    "Mix the ingredients. Cook in a lightly oiled pan until golden.",
                    20,
                    category_ids["Breakfast"]
                ),
                (
                    "Greek Salad",
                    "Tomatoes, cucumber, feta, olives, olive oil",
                    "Chop vegetables, add feta and olives, then dress with olive oil.",
                    15,
                    category_ids["Lunch"]
                ),
                (
                    "Garlic Tomato Pasta",
                    "Pasta, tomatoes, garlic, olive oil, basil",
                    "Boil pasta. Cook garlic and tomatoes, combine, and add basil.",
                    30,
                    category_ids["Dinner"]
                ),
                (
                    "Chocolate Mug Cake",
                    "Flour, cocoa, sugar, milk, oil",
                    "Mix in a microwave-safe mug and microwave for 60–90 seconds.",
                    5,
                    category_ids["Desserts"]
                )
            ]

            db.executemany(
                """
                INSERT INTO recipes (
                    title, ingredients, instructions,
                    cooking_time, category_id
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                sample_recipes
            )