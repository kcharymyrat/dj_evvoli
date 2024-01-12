# pull official base image
FROM python:3.11.1-bullseye

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --no-cache-dir pip==23.3.1

# Copy the requirements directory
COPY requirements /usr/src/app/requirements

# Install Python dependencies
ARG REQUIREMENTS_FILE
RUN pip install -r ${REQUIREMENTS_FILE}

# copy project
COPY . .