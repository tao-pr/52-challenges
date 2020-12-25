#!/bin/bash

# -d for detach from terminal
# joins the same network as Cassandra 
docker run -d -p 3334:3334 --network n1 --name nodecass nodecass:v1