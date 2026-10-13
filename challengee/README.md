# Online Recipe Book

A recipe management application built with FastAPI, Streamlit,
SQLite, Requests, and Python Dotenv.

## Features

- View recipes and categories
- Add, edit, and delete recipes
- Add, edit, and delete categories
- Search and filter recipes
- Store data in SQLite
- Explore API endpoints using Swagger

## Installation

Install the dependencies:

pip install -r requirements.txt

## Run the backend

uvicorn app:app --reload

API documentation:
http://127.0.0.1:8000/docs

## Run the frontend

Open a second terminal:

streamlit run main.py

Application:
http://localhost:8501