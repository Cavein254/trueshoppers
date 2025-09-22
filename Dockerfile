FROM python:3.12-bullseye

# set a directory for the app
WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
# Copy base requirement file
COPY requirements.txt .
# Copy development requirement file
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# Copy Django project
COPY . .

# collect static
RUN python manage.py collectstatic --noinput --settings=core.settings.dev

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose Django default port
EXPOSE 8000

# Start Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
