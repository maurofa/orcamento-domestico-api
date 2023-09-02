# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.11-alpine

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install the requirements
COPY requirements-docker.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements-docker.txt

COPY . .

EXPOSE 5000/tcp

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
