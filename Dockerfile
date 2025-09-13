FROM python:3.12-bullseye

# set a directory for the app
WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc curl netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x ./entrypoint.sh

# Copy Django project
COPY . .


# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Expose Django default port
EXPOSE 8000

# Start Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
