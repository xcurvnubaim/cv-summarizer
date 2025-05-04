# Install uv
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable

# Copy the project into the intermediate image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable

# Compile Python scripts to bytecode
RUN python -m compileall -b /app/src

FROM python:3.12-slim

# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder /app/src /app/src

COPY data/data-oprec.csv /data/data-oprec.csv

# Set the Python virtual environment path
ENV PATH="/app/.venv/bin:$PATH"

# Run the application
CMD ["python", "/app/src/main.pyc"]