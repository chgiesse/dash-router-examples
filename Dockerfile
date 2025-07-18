FROM python:3.12-slim-bookworm

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false
# Copy poetry.lock if it exists, otherwise generate it
COPY poetry.lock* ./
RUN poetry lock --no-update || poetry lock
RUN poetry install --no-interaction --no-ansi

# Copy application code
COPY app/. /app

# Create nonroot user
RUN groupadd -r nonroot && \
    useradd -r -g nonroot nonroot
RUN chown -R nonroot:nonroot /app
USER nonroot

# Expose port
EXPOSE 8050
ENV PG_ENGINE_STR='postgresql+asyncpg://datenschubse:E7h2Jtg4RSw57XfRILZ5c6KvAPszefQb@dpg-d1l7dvje5dus73fbg4gg-a.frankfurt-postgres.render.com/dash_example'

# Use gunicorn for production deployment with standard Dash/Flask
ENTRYPOINT ["python", "-m", "uvicorn", "app:server", "--host", "0.0.0.0", "--port", "8050", "--workers", "2", "--timeout-keep-alive", "30", "--log-level", "error"]            
