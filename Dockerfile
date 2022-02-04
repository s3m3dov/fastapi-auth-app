# Pull base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade -r /code/requirements.txt

# Copy project
COPY . /code/

