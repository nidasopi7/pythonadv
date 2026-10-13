from fastapi import APIRouter, HTTPException, Response

from database import get_db
from models.recipe import RecipeCreate, RecipeUpdate

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)


def recipe_query():
    return """
        SELECT r.*, c.name AS category_name
        FROM recipes r
        JOIN categories c ON c.id = r.category_id
    """


def check_category(db, category_id):
    row = db.execute(
        "SELECT id FROM categories WHERE id = ?",
        (category_id,)
    ).fetchone()

    if row is None:
        raise HTTPException(400, "Category does not exist")


@router.get("/")
def list_recipes(
    category_id: int | None = None,
    search: str = ""
):
    query = recipe_query()
    conditions = []
    params = []

    if category_id is not None:
        conditions.append("r.category_id = ?")
        params.append(category_id)

    if search.strip():
        conditions.append("r.title LIKE ?")
        params.append(f"%{search.strip()}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY r.id DESC"

    with get_db() as db:
        rows = db.execute(query, params).fetchall()
        return [dict(row) for row in rows]


@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    with get_db() as db:
        row = db.execute(
            recipe_query() + " WHERE r.id = ?",
            (recipe_id,)
        ).fetchone()

        if row is None:
            raise HTTPException(404, "Recipe not found")

        return dict(row)


@router.post("/", status_code=201)
def create_recipe(recipe: RecipeCreate):
    title = recipe.title.strip()

    if not title:
        raise HTTPException(422, "Recipe title is required")

    with get_db() as db:
        check_category(db, recipe.category_id)

        cursor = db.execute(
            """
            INSERT INTO recipes (
                title, ingredients, instructions,
                cooking_time, category_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                title,
                recipe.ingredients.strip(),
                recipe.instructions.strip(),
                recipe.cooking_time,
                recipe.category_id
            )
        )

        row = db.execute(
            recipe_query() + " WHERE r.id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        return dict(row)


@router.put("/{recipe_id}")
def update_recipe(recipe_id: int, recipe: RecipeUpdate):
    title = recipe.title.strip()

    if not title:
        raise HTTPException(422, "Recipe title is required")

    with get_db() as db:
        existing = db.execute(
            "SELECT id FROM recipes WHERE id = ?",
            (recipe_id,)
        ).fetchone()

        if existing is None:
            raise HTTPException(404, "Recipe not found")

        check_category(db, recipe.category_id)

        db.execute(
            """
            UPDATE recipes
            SET title = ?, ingredients = ?, instructions = ?,
                cooking_time = ?, category_id = ?
            WHERE id = ?
            """,
            (
                title,
                recipe.ingredients.strip(),
                recipe.instructions.strip(),
                recipe.cooking_time,
                recipe.category_id,
                recipe_id
            )
        )

        row = db.execute(
            recipe_query() + " WHERE r.id = ?",
            (recipe_id,)
        ).fetchone()

        return dict(row)


@router.delete("/{recipe_id}", status_code=204)
def delete_recipe(recipe_id: int):
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM recipes WHERE id = ?",
            (recipe_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(404, "Recipe not found")

    return Response(status_code=204)