# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
# ENV UV_COMPILE_BYTECODE=1
# ENV UV_LINK_MODE=copy
# ENV UV_HTTP_TIMEOUT=120
# WORKDIR /app

# COPY pyproject.toml uv.lock ./
# COPY services/product-service/pyproject.toml services/product-service/

# RUN uv venv /app/.venv
# RUN uv sync --package product-service --frozen --no-dev

# COPY . .

# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
# WORKDIR /app

# COPY --from=builder /app/.venv /app/.venv
# COPY --from=builder /app/services /app/services

# ENV PATH="/app/.venv/bin:$PATH"

# ENV PYTHONPATH="/app/services/product-service"

# CMD ["python", "services/product-service/main.py"]

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./
COPY services/product_service/pyproject.toml services/product_service/

# Install dependencies
RUN uv sync --package product_service --frozen --no-dev --python 3.13

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

CMD ["python", "services/product_service/main.py"]