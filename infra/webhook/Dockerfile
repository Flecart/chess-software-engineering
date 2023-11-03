FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt update && apt install --no-install-recommends sudo

RUN pip install flask

COPY webhook.py ./webhook.py

EXPOSE 80

ENTRYPOINT ["python", "webhook.py"]
