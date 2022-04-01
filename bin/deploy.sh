#!/bin/bash

make pg_dump
git stash & git pull
docker-compose up --build --force-recreate -d
docker-compose exec -T bot alembic upgrade head