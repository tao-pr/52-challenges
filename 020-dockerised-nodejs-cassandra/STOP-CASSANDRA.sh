#!/bin/bash

CID=$(docker container ls -a | grep cassandra |  awk '{print $1}' | head -1)
echo "terminating cassandra docker container ..."
docker container stop $CID
echo "[stopped]"
docker container rm $CID
echo "[terminated]"