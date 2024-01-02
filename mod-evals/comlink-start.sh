#!/bin/sh

echo "Starting swgoh-comlink"
docker pull ghcr.io/swgoh-utils/swgoh-comlink:latest
docker network create swgoh-comlink
docker run --name swgoh-comlink \
  -d \
  --restart always \
  --network swgoh-comlink \
  --env APP_NAME=$APP_NAME \
  -p 3200:3000 \
  ghcr.io/swgoh-utils/swgoh-comlink:latest