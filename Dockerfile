# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
# WORKDIR /app

# Copy the requirements.txt file into the container
COPY ./requirements.txt /app/requirements.txt

# Install Python packages specified in requirements.txt
# --no-cache-dir helps reduce the image size
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY ./app /app
# If you have a .env file and want it in the container, uncomment and ensure it's in the root of your project
COPY ./.venv /.env

# Expose the port the app runs on
EXPOSE 8000

# Run the Uvicorn server when the container starts
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]