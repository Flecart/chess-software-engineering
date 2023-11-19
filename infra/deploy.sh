#!/bin/bash
git checkout deploy
git pull
sudo docker compose up -d --build --force-recreate
