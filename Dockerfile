# Base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Expose the port on which the Flask application runs (if applicable)
EXPOSE 5000

# Set the entrypoint command to run the Flask application
CMD ["python", "main.py"]
