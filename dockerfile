# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN --mount=type=cache,id=s/a689ff66-ae9d-4bd9-a704-f29f4664dc11-/root/cache/pip,target=/root/.cache/pip python -m venv --copies /opt/venv && . /opt/venv/bin/activate && pip install -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1
ENV NIXPACKS_PATH=/opt/venv/bin:$NIXPACKS_PATH

# Run the command to start Gunicorn
CMD ["gunicorn", "IRiseUpAi.wsgi:application", "--log-file", "-"]
