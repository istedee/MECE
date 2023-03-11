#!/bin/bash

echo
echo "Starting up Docker container for curses client"

sudo docker compose up --build -d > /dev/null 2>&1

echo "Docker container build complete"

sleep 1

echo
echo "Starting up the client on the docker host"
echo

sleep 2

sudo docker exec -it curses-client python3 tha_client.py