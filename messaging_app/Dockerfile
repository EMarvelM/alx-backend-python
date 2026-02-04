# Use a base Python image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies (for mysqlclient)
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port (default 8000)
EXPOSE 8000

# Run gunicorn (or manage.py runserver for dev, but CMD is standard)
# We'll use a simple command for now, can be overridden by docker-compose
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
