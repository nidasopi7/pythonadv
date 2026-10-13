from pydantic import BaseModel, Field


class RecipeCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    ingredients: str = Field(min_length=1)
    instructions: str = Field(min_length=1)
    cooking_time: int = Field(default=30, ge=1, le=1440)
    category_id: int = Field(gt=0)


class RecipeUpdate(RecipeCreate):
    pass