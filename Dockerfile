FROM python:3.9-slim

WORKDIR /app

COPY . .

# dependencies
RUN python3 -m pip install --upgrade pip \
	&& python3 -m pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install