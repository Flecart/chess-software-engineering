FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt update && apt install -y --no-install-recommends sudo git

RUN addgroup --gid 1000 nonroot && \
    adduser --uid 1000 --gid 1000 --disabled-password --gecos "" nonroot && \
    echo 'nonroot ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers

USER nonroot

RUN git config --global --add safe.directory /app/deploy

RUN pip install flask

COPY webhook.py monitor.py ./

EXPOSE 80

ENTRYPOINT ["python", "webhook.py"]
