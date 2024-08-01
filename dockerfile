# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
ADD Practice .

RUN cd analytics_master

# Install the dependencies
RUN pip install --no-cache-dir -r /app/analytics_master/requirements.txt

# Expose the port FastAPI will run on
EXPOSE 500

# Command to run the FastAPI application using Uvicorn

CMD ["uvicorn", "/app/analytics_master/main:app", "--host", "0.0.0.0", "--port", "5000"]
