# Task_management_API
## Overview
This is a web application built with Django for managing tasks. The application allows users to reserve spots in a resturant.

Users are required to authenticate using their email and password, and only authenticated users can interact with the website.

## Features
- **User Authentication:**
  - Users can register and access tasks after authentication using JWT (JSON Web Tokens).
  - Token-based authentication with `rest_framework_simplejwt`.
- **Task Management:**
  - Users can create tasks with fields like `status`, `priority`, and `due_date`.
  - Users can read, update, and delete their own tasks.
- **Task Filtering:**
  - Users can filter tasks by `status`, `priority`, and `due_date`.
- **User Profiles:**
  - Users can retrieve their own profile at `/api/users/me/`.
  
## Endpoints
### User Endpoints
- **POST** `/api/auth/register/` - Register a new user.
- **POST** `/api/token/` - Obtain a JWT token for authentication.
- **GET** `/api/users/me/` - Retrieve the authenticated user's profile.

### Task Endpoints
- **POST** `/api/tasks/` - Create a new task.
- **GET** `/api/tasks/` - Retrieve all tasks for the authenticated user.
- **GET** `/api/tasks/{id}/` - Retrieve a specific task by ID.
- **PUT** `/api/tasks/{id}/` - Update an existing task by ID.
- **DELETE** `/api/tasks/{id}/` - Delete a task by ID.

## Prerequisites
- Python 3.10 
- pip (Python package installer)
- VS Code
## Clone the Repository
git clone https://github.com/Bisruxa/Task_management_API.git
# Navigate to the project directory: 
cd Task_management_API
## create and activate a virtual environment
use "python -m venv venv" to create
use "source venv/Scripts/activate" to activate 
## install django and create django project 
pip install django 
django-admin startproject Task_managemnt . 
## run migrations
python manage.py makemigrations
python manage.py migarte
## run server
python manage.py runserver
