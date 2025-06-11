# from python 3.13 chainguard image
FROM chainguard/python:3.13-dev AS dev

WORKDIR /app

RUN python -m venv .venv

ENV PATH=/app/.venv/bin:$PATH

COPY uv.lock /app/
COPY pyproject.toml /app/

# run uv sync
RUN uv sync --no-dev --frozen

# get production image
FROM chainguard/python:3.13

WORKDIR /app

COPY . /app/
COPY --from=dev /app/.venv /app/.venv

ENV PATH=/app/.venv/bin:$PATH

EXPOSE 2024

CMD [ "langgraph", "dev" ]
