# Task Manager API

A robust and scalable FastAPI application designed to manage tasks. This API provides full CRUD (Create, Read, Update, Delete) capabilities for tasks,
with data persisted in a PostgreSQL database. The project is structured for maintainability, containerized with Docker for consistent environments,
and set up for GitOps deployment to a Kubernetes cluster on Oracle Cloud Infrastructure (OCI) Arm nodes using ArgoCD.

## Features

* **RESTful API:** Provides standard HTTP methods (GET, POST, PUT, PATCH, DELETE) for task management.
* **PostgreSQL Database:** Data is persistently stored in a robust PostgreSQL database.
* **SQLAlchemy ORM:** Utilizes SQLAlchemy 2.0 as an Object-Relational Mapper for efficient and Pythonic database interactions.
* **Pydantic Models:** Ensures robust data validation and serialization for API requests and responses.
* **Modular Architecture:** Code is organized into dedicated modules (`models`, `schemas`, `crud`, `routers`) for improved maintainability and scalability.
* **CRUD Operations:** Full Create, Read, Update, and Delete functionality for tasks.
* **Containerized Development:** Local development environment managed using Docker Compose, providing isolated and consistent setups.
* **Hot-Reloading:** Code changes are automatically reflected during local development via Docker Compose volumes and Uvicorn's reload feature.

## Prerequisites

Before you begin, ensure you have the following installed on your local machine:

* **Docker:** Used for containerizing the application and database.
    * [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
* **Docker Compose:** Typically comes bundled with Docker Desktop.
* **Git:** For cloning the repository.
    * [Download Git](https://git-scm.com/downloads)
* **Python 3.x:** (Optional, for managing `requirements.txt` and `venv` outside of Docker, though Docker will handle the primary runtime environment for the app.)
    * [Download Python](https://www.python.org/downloads/)

## Local Development Setup

Follow these steps to set up and run the Task Manager API locally using Docker Compose:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/HowDiggy/task-manager-api
    cd task-manager-api
    ```

2.  **Verify `requirements.txt`:**
    Ensure your `requirements.txt` file contains the necessary Python dependencies. It should look like this:
    ```
    fastapi==0.115.13
    uvicorn==0.34.3
    sqlalchemy==2.0.41
    psycopg2-binary==2.9.10
    pydantic==2.11.7
    ```
    *(Note: You can update these versions if newer stable releases are available, but ensure compatibility.)*

3.  **Verify `Dockerfile`:**
    Confirm your `Dockerfile` is set up for Python 3.12 (or your chosen version) and the correct `WORKDIR` and `COPY` paths for the multi-stage build:
    ```dockerfile
    # Dockerfile
    # Stage 1: Build Stage - Install dependencies
    FROM python:3.12-slim-bookworm AS builder
    WORKDIR /usr/src/app
    COPY requirements.txt .
    RUN pip install --upgrade pip && \
        pip install --no-cache-dir -r requirements.txt

    # Stage 2: Final Stage - Copy app code and run
    FROM python:3.12-slim-bookworm
    WORKDIR /usr/src/app
    COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
    COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
    COPY . .
    EXPOSE 8000
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    ```

4.  **Verify `app/database.py`:**
    Ensure your database connection string in `app/database.py` points to the `db` service (as defined in `docker-compose.yml`):
    ```python
    # app/database.py
    # ...
    SQLALCHEMY_DATABASE_URL = "postgresql://user:mysecretpassword@db:5432/taskmanagerdb"
    # ...
    ```

5.  **Build and Run with Docker Compose:**
    Navigate to the root of your `task-manager-api` directory in your terminal and run:
    ```bash
    docker compose up --build -d
    ```
    * `--build`: Forces Docker Compose to rebuild the `app` service image, ensuring your latest code and `Dockerfile` changes are included.
    * `-d`: Runs the containers in detached mode (in the background).

6.  **Verify Running Containers:**
    Check that both your database and application containers are running:
    ```bash
    docker ps
    ```
    You should see `task-manager-postgres` and `task-manager-api-app` listed.

7.  **Access the API:**
    Open your web browser and navigate to the interactive API documentation (Swagger UI):
    ```
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    ```
    You can now use this interface to test all your API endpoints.

## Project Structure
The project is organized into a modular and maintainable structure, separating concerns into distinct Python packages
and modules within the `app/` directory:
```
task-manager-api/
├── app/                              # The main application package
│   ├── init.py                   # Makes 'app' a Python package
│   ├── main.py                       # FastAPI app instance, includes routers
│   ├── database.py                   # SQLAlchemy engine, session, and dependency (get_db)
│   ├── models.py                     # SQLAlchemy ORM models (e.g., DBTask)
│   ├── schemas.py                    # Pydantic models (e.g., Task, TaskBase)
│   ├── crud.py                       # Database (CRUD) operations logic
│   └── routers/                      # Directory for API routers (endpoints)
│       ├── init.py               # Makes 'routers' a Python package
│       └── tasks.py                  # API endpoints related to tasks (using APIRouter)
│
├── docker-compose.yml              # Defines local development services (app & db)
├── Dockerfile                      # Instructions for building the FastAPI application's Docker image
└── requirements.txt                # Python dependency list
```
## API Endpoints

The API provides the following endpoints for managing tasks:

* **`POST /tasks/`**: Create a new task.
* **`GET /tasks/`**: Retrieve a list of all tasks (with optional `skip` and `limit` for pagination).
* **`GET /tasks/{task_id}`**: Retrieve a single task by its UUID.
* **`PUT /tasks/{task_id}`**: Fully update an existing task by its UUID.
* **`PATCH /tasks/{task_id}`**: Partially update an existing task by its UUID.
* **`DELETE /tasks/{task_id}`**: Delete a task by its UUID.

All endpoints are self-documented and interactive via the Swagger UI at `http://127.0.0.1:8000/docs`.

## Future Enhancements

* **Authentication & Authorization:** Implement user authentication (e.g., JWT) and role-based access control.
* **Unit and Integration Tests:** Add a comprehensive test suite using `pytest`.
* **Logging and Monitoring:** Integrate more advanced logging and metrics collection.
* **Error Handling:** Implement custom exception handlers for more graceful API error responses.
* **More Features:** Add support for task categories, due dates, user assignments, etc.
