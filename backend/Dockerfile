# --- Build Stage ---
FROM python:3.12-slim AS builder

# Install uv by copying the standalone binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Match the runtime stage directory path here to keep virtualenv paths intact
WORKDIR /code
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency definitions first to maximize Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into the virtual environment (.venv)
RUN uv sync --frozen --no-install-project --no-dev

# --- Runtime Stage ---
FROM python:3.12-slim

WORKDIR /code

# Copy the pre-built virtual environment from the builder stage
COPY --from=builder /code/.venv /code/.venv

# Copy your actual application source code
COPY ./app /code/app

# Place the virtual environment's executables directly onto the PATH
ENV PATH="/code/.venv/bin:$PATH"

# Create and switch to a non-root user for security compliance
RUN useradd -m appuser && chown -R appuser:appuser /code
USER appuser

EXPOSE 8000

# Run Uvicorn directly out of the activated PATH environment
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
