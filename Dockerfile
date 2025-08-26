# -----------------------------
# Stage 1: Builder
# -----------------------------
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy project files for dependency installation
COPY pyproject.toml poetry.lock* ./

# Install only production dependencies, skip installing the project itself
RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi --no-root

# Copy the rest of the project
COPY . .

# Collect static files for Django
RUN python manage.py collectstatic --noinput


# -----------------------------
# Stage 2: Final Image
# -----------------------------
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*
RUN pip install gunicorn

# Copy installed Python packages and project from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /app /app

# Expose application port
EXPOSE 8000


ENV DEBUG=true
ENV ENVIRONMENT=KUBERNETES

# Run Gunicorn server
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:80", "sailors_log.wsgi:application", "--paste", "static:/app/staticfiles"]
