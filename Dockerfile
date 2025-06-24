# Dockerfile

# Stage 1: Build Stage - Install dependencies
FROM python:3.12-slim-bookworm AS builder

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Final Stage - Copy app code and run
FROM python:3.12-slim-bookworm

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Copy only the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy the entire application code into the container
# The '.' means copy everything from the current build context (task-manager-api directory)
# to the WORKDIR (/usr/src/app) inside the container.
COPY . .

# Expose the port your FastAPI application will run on
EXPOSE 8000

# Command to run your FastAPI application using Uvicorn
# Now that `app` directory is directly under WORKDIR, 'app.main:app' will work.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]