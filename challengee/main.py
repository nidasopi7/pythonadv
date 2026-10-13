
import os

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv(
    "API_URL", "http://127.0.0.1:8000"
).rstrip("/")

st.set_page_config(
    page_title="Online Recipe Book",
    page_icon="🍲",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #faf9f6;
}
h1, h2, h3 {
    color: #315447;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #e8e5dd;
}
</style>
""", unsafe_allow_html=True)


def api_request(method, path, **kwargs):
    try:
        response = requests.request(
            method,
            f"{API_URL}{path}",
            timeout=10,
            **kwargs
        )

        if not response.ok:
            try:
                detail = response.json().get(
                    "detail", response.text
                )
            except ValueError:
                detail = response.text

            st.error(
                f"API error ({response.status_code}): {detail}"
            )
            return None

        if response.status_code == 204:
            return True

        return response.json()

    except requests.RequestException:
        st.error(
            "Cannot connect to the API. Start FastAPI first "
            "using: uvicorn app:app --reload"
        )
        return None


def load_categories():
    return api_request("GET", "/categories/") or []


def load_recipes(category_id=None, search=""):
    params = {}

    if category_id is not None:
        params["category_id"] = category_id

    if search.strip():
        params["search"] = search.strip()

    return api_request(
        "GET", "/recipes/", params=params
    ) or []


st.sidebar.title("🍲 Recipe Book")
st.sidebar.caption("Your personal kitchen companion")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Manage Recipes",
        "Manage Categories"
    ]
)

categories = load_categories()
category_map = {
    category["name"]: category["id"]
    for category in categories
}


# ---------------- DASHBOARD ----------------

if page == "Dashboard":
    st.title("🍲 Online Recipe Book")
    st.write(
        "Discover, organize, and manage your favorite recipes."
    )

    recipes = load_recipes()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Recipes", len(recipes))
    col2.metric("Categories", len(categories))

    average = (
        round(
            sum(r["cooking_time"] for r in recipes)
            / len(recipes)
        )
        if recipes else 0
    )

    col3.metric("Average Cooking Time", f"{average} min")

    st.subheader("Recipe Collection")

    search = st.text_input("🔎 Search recipes by title")

    selected_category = st.selectbox(
        "Filter by category",
        ["All categories"] + list(category_map.keys())
    )

    category_id = (
        category_map[selected_category]
        if selected_category != "All categories"
        else None
    )

    filtered = load_recipes(category_id, search)

    if filtered:
        st.dataframe(
            [
                {
                    "ID": r["id"],
                    "Recipe": r["title"],
                    "Category": r["category_name"],
                    "Cooking Time (min)": r["cooking_time"],
                    "Ingredients": r["ingredients"]
                }
                for r in filtered
            ],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Recipe Details")

        selected_recipe = st.selectbox(
            "Choose a recipe to view",
            filtered,
            format_func=lambda r: r["title"]
        )

        if selected_recipe:
            with st.container(border=True):
                st.subheader(selected_recipe["title"])
                st.caption(
                    f"{selected_recipe['category_name']} · "
                    f"{selected_recipe['cooking_time']} minutes"
                )

                st.markdown("**Ingredients**")
                st.write(selected_recipe["ingredients"])

                st.markdown("**Instructions**")
                st.write(selected_recipe["instructions"])

    else:
        st.info("No recipes found. Add a recipe to get started.")


# ---------------- MANAGE RECIPES ----------------

elif page == "Manage Recipes":
    st.title("📝 Manage Recipes")

    tab_add, tab_edit, tab_delete = st.tabs(
        ["➕ Add Recipe", "✏️ Edit Recipe", "🗑️ Delete Recipe"]
    )

    with tab_add:
        st.subheader("Add a New Recipe")

        if not categories:
            st.warning("Create a category before adding a recipe.")
        else:
            with st.form("add_recipe_form", clear_on_submit=True):
                title = st.text_input("Recipe title")
                ingredients = st.text_area("Ingredients")
                instructions = st.text_area("Instructions")

                cooking_time = st.number_input(
                    "Cooking time (minutes)",
                    min_value=1,
                    max_value=1440,
                    value=30
                )

                category_name = st.selectbox(
                    "Category",
                    list(category_map.keys())
                )

                submitted = st.form_submit_button(
                    "Add Recipe",
                    type="primary"
                )

                if submitted:
                    if not all([
                        title.strip(),
                        ingredients.strip(),
                        instructions.strip()
                    ]):
                        st.error("Please complete all recipe fields.")
                    else:
                        result = api_request(
                            "POST",
                            "/recipes/",
                            json={
                                "title": title.strip(),
                                "ingredients": ingredients.strip(),
                                "instructions": instructions.strip(),
                                "cooking_time": int(cooking_time),
                                "category_id": category_map[category_name]
                            }
                        )

                        if result:
                            st.success("Recipe added successfully!")
                            st.rerun()

    with tab_edit:
        recipes = load_recipes()

        if not recipes:
            st.info("No recipes available to edit.")
        elif not categories:
            st.warning("Create a category first.")
        else:
            chosen = st.selectbox(
                "Choose a recipe to edit",
                recipes,
                format_func=lambda r: r["title"],
                key="edit_recipe"
            )

            with st.form("edit_recipe_form"):
                new_title = st.text_input(
                    "Recipe title",
                    value=chosen["title"]
                )

                new_ingredients = st.text_area(
                    "Ingredients",
                    value=chosen["ingredients"]
                )

                new_instructions = st.text_area(
                    "Instructions",
                    value=chosen["instructions"]
                )

                new_time = st.number_input(
                    "Cooking time (minutes)",
                    min_value=1,
                    max_value=1440,
                    value=int(chosen["cooking_time"])
                )

                names = list(category_map.keys())
                old_category = chosen["category_name"]

                category_index = (
                    names.index(old_category)
                    if old_category in names else 0
                )

                new_category = st.selectbox(
                    "Category",
                    names,
                    index=category_index
                )

                save = st.form_submit_button(
                    "Save Changes",
                    type="primary"
                )

                if save:
                    if not all([
                        new_title.strip(),
                        new_ingredients.strip(),
                        new_instructions.strip()
                    ]):
                        st.error("Please complete all recipe fields.")
                    else:
                        result = api_request(
                            "PUT",
                            f"/recipes/{chosen['id']}",
                            json={
                                "title": new_title.strip(),
                                "ingredients": new_ingredients.strip(),
                                "instructions": new_instructions.strip(),
                                "cooking_time": int(new_time),
                                "category_id": category_map[new_category]
                            }
                        )

                        if result:
                            st.success("Recipe updated successfully!")
                            st.rerun()

    with tab_delete:
        recipes = load_recipes()

        if not recipes:
            st.info("No recipes available to delete.")
        else:
            chosen = st.selectbox(
                "Choose a recipe to delete",
                recipes,
                format_func=lambda r: r["title"],
                key="delete_recipe"
            )

            confirm = st.checkbox(
                "I confirm that I want to delete this recipe",
                key="confirm_delete_recipe"
            )

            if st.button("Delete Recipe", type="primary"):
                if not confirm:
                    st.warning("Please confirm deletion first.")
                else:
                    result = api_request(
                        "DELETE",
                        f"/recipes/{chosen['id']}"
                    )

                    if result:
                        st.success("Recipe deleted successfully!")
                        st.rerun()


# ---------------- MANAGE CATEGORIES ----------------

elif page == "Manage Categories":
    st.title("📂 Manage Categories")

    tab_add, tab_edit, tab_delete = st.tabs(
        ["➕ Add Category", "✏️ Edit Category", "🗑️ Delete Category"]
    )

    with tab_add:
        with st.form("add_category_form", clear_on_submit=True):
            name = st.text_input("Category name")
            description = st.text_area("Description (optional)")

            submitted = st.form_submit_button(
                "Add Category",
                type="primary"
            )

            if submitted:
                if not name.strip():
                    st.error("Category name is required.")
                else:
                    result = api_request(
                        "POST",
                        "/categories/",
                        json={
                            "name": name.strip(),
                            "description": description.strip()
                        }
                    )

                    if result:
                        st.success("Category added successfully!")
                        st.rerun()

    with tab_edit:
        if not categories:
            st.info("No categories available to edit.")
        else:
            chosen = st.selectbox(
                "Choose a category to edit",
                categories,
                format_func=lambda c: c["name"],
                key="edit_category"
            )

            with st.form("edit_category_form"):
                new_name = st.text_input(
                    "Category name",
                    value=chosen["name"]
                )

                new_description = st.text_area(
                    "Description",
                    value=chosen["description"] or ""
                )

                save = st.form_submit_button(
                    "Save Changes",
                    type="primary"
                )

                if save:
                    if not new_name.strip():
                        st.error("Category name is required.")
                    else:
                        result = api_request(
                            "PUT",
                            f"/categories/{chosen['id']}",
                            json={
                                "name": new_name.strip(),
                                "description": new_description.strip()
                            }
                        )

                        if result:
                            st.success("Category updated successfully!")
                            st.rerun()

    with tab_delete:
        if not categories:
            st.info("No categories available to delete.")
        else:
            chosen = st.selectbox(
                "Choose a category to delete",
                categories,
                format_func=lambda c: c["name"],
                key="delete_category"
            )

            st.warning(
                "Categories containing recipes cannot be deleted."
            )

            confirm = st.checkbox(
                "I confirm that I want to delete this category",
                key="confirm_delete_category"
            )

            if st.button("Delete Category", type="primary"):
                if not confirm:
                    st.warning("Please confirm deletion first.")
                else:
                    result = api_request(
                        "DELETE",
                        f"/categories/{chosen['id']}"
                    )

                    if result:
                        st.success("Category deleted successfully!")
                        st.rerun()