# get production image
FROM python:3.13-slim

RUN pip install uv

WORKDIR /app

RUN python -m venv .venv

ENV PATH=/app/.venv/bin:$PATH

COPY . /app/

# run uv sync
RUN uv sync --no-dev --frozen

EXPOSE 2024

CMD [ "langgraph", "dev" ]
