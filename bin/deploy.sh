#!/bin/bash

make pg_dump
git stash & git pull
docker-compose up --build --force-recreate -d