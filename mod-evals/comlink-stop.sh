#!/bin/sh

echo "Stopping swgoh-comlink"
docker stop swgoh-comlink
docker rm swgoh-comlink
docker network rm swgoh-comlink