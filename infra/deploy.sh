#!/bin/bash
git checkout main
git pull
sudo docker compose up -d --build --force-recreate
sudo docker builder prune -af
