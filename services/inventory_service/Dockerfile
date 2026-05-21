FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY services/inventory_service/pyproject.toml services/inventory_service/
RUN uv sync --package inventory_service --frozen --no-dev --python 3.13
COPY . .

FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
WORKDIR /app
COPY --from=builder /app /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

CMD ["uvicorn", "services.inventory_service.main:app", "--host", "0.0.0.0", "--port", "8000"]