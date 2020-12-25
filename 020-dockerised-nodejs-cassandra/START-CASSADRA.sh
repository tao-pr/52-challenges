#!/bin/bash

# See instructions for cassandra docker on:
# https://hub.docker.com/_/cassandra
docker run --name c1 --network n1  -p 9042:9042 -d cassandra:latest