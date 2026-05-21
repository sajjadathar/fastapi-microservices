# # Stage 1: The Builder
# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
# WORKDIR /app

# # Copy the dependencies files first for docker caching
# COPY pyproject.toml uv.lock ./

# # Copy the specific service files
# COPY services/user-service/pyproject.toml services/user-service/

# # Install dependencies for the user service
# RUN uv sync --package user-service --frozen --no-dev --python 3.13

# # Copy the rest of the code
# COPY . .

# # Stage 2: The Final Image
# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
# WORKDIR /app

# # Copy the environment and code from the builder
# COPY --from=builder /app /app

# # Put the virtual environment on the path
# ENV PATH="/app/.venv/bin:$PATH"

# ENV PYTHONPATH="/app/services/user-service:/app"

# # Run the FastAPI server
# CMD ["fastapi", "run", "services/user-service/main.py", "--port", "8000", "--host", "0.0.0.0"]

######################################################
# Stage 1: Builder
# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# WORKDIR /app

# COPY pyproject.toml uv.lock ./
# COPY services/user_service/pyproject.toml services/user_service/

# RUN uv sync --package user_service --frozen --no-dev --python 3.13

# COPY . .

# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# WORKDIR /app

# COPY --from=builder /app/.venv /app/.venv
# COPY --from=builder /app/services /app/services
# COPY --from=builder /app/shared /app/shared   

# ENV PATH="/app/.venv/bin:$PATH"
# ENV PYTHONPATH="/app"

# EXPOSE 8000

# CMD ["uvicorn", "services.user_service.main:app", "--host", "0.0.0.0", "--port", "8000"]



FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./
COPY services/user_service/pyproject.toml services/user_service/

# Install dependencies
RUN uv sync --package user_service --frozen --no-dev --python 3.13

# Copy full project (needed for proto compilation)
COPY . .

# ============================
# Generate gRPC files (BUILD TIME)
# ============================
RUN uv run python -m grpc_tools.protoc \
    -I protos \
    --python_out=. \
    --grpc_python_out=. \
    protos/product.proto

# ============================
# FINAL RUNTIME IMAGE
# ============================
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/services /app/services
COPY --from=builder /app/shared /app/shared
COPY --from=builder /app/*.py /app/

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

EXPOSE 8000

CMD ["uvicorn", "services.user_service.main:app", "--host", "0.0.0.0", "--port", "8000"]