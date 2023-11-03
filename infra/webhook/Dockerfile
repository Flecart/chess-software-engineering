FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt update && apt install -y --no-install-recommends sudo git

RUN git config --global --add safe.directory /app/deploy

RUN pip install flask

COPY webhook.py ./webhook.py

EXPOSE 80

ENTRYPOINT ["python", "webhook.py"]
