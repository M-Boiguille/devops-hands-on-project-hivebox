FROM python:3.12-slim AS builder

WORKDIR /app

RUN useradd -m appuser

USER appuser

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r \
  /app/requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /home/appuser/.local \
  /home/appuser/.local/

COPY Dockerfile main.py helpers.py config.json /app/

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8080

CMD ["fastapi", "run", "/app/main.py", "--port", "80"]
