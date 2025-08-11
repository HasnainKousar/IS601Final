
# FinalProject

## Overview

This is a FastAPI-based web application for user management and performing calculations. It supports user registration, login, and CRUD operations for calculations. The app uses a database for storing users and calculations, and provides a simple web interface.

## Features

- User registration and login
- JWT-based authentication
- CRUD operations for calculations
- Web dashboard for users
- Health check endpoint
- Docker support for easy deployment
- Automated tests (unit, integration, e2e)

## Project Structure

```
app/
  ├── main.py            # Main FastAPI app
  ├── models/            # Database models (user, calculation)
  ├── schemas/           # Pydantic schemas for API
  ├── auth/              # Authentication logic (JWT, dependencies)
  ├── core/              # Config and core utilities
  ├── operations/        # Business logic
  ├── database.py        # Database connection
  ├── database_init.py   # DB initialization
static/                  # CSS and JS files
templates/               # HTML templates
tests/                   # Test suite (unit, integration, e2e)
docker-compose.yml       # Docker Compose config
Dockerfile               # Dockerfile for building image
requirements.txt         # Python dependencies
```

## How to Run the Application

1. Make sure you have Docker installed.
2. Build and start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. The application will be available at `http://localhost:8000` (or the port specified in your configuration).

## How to Run Tests Locally

1. Make sure you have Python and `pip` installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run tests using pytest:
   ```bash
   pytest
   ```

## Docker Hub Repository

You can find the Docker image for this project at:

[Docker Hub - final_project](https://hub.docker.com/repository/docker/hkousar13/final_project/general)
