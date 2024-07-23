# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT=8000

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install utils
RUN apk update
RUN apk upgrade
RUN apk add bash
RUN apk add \
  build-base \
  gcc \
  libc-dev \
  linux-headers \
  python3-dev \
  musl-dev \
  libffi-dev

# Use the custom entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Install the project dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on
EXPOSE ${PORT}

# Start the application
CMD ["python", "manage.py", "runserver"]
