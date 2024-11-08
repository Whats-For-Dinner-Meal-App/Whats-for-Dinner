from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(String)
    instructions = Column(String)
    '''
    Other column ideas: 
    category: Categorizes recipes (like “breakfast” or “dinner”) to make filtering easier.
    prep_time and cook_time: Holds the preparation and cooking times, respectively, in minutes.
    servings: Number of servings the recipe makes, helpful for meal planning.
    author_id: If your app allows users to add recipes, this could be a foreign key reference to a users table.
    created_at and updated_at: Timestamps for when the recipe was created or last updated, useful for sorting or tracking recipe edits.
    img_url: A URL to an image of the finished dish, if you want to display images in the app.
    '''