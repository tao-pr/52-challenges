# Dockerised NodeJS App + Cassandra

Interfacing NodeJS with Cassadra and make them containers.

## Prerequisites

- Docker

## Setup

Run a setup script to prepare docker network interface.

```bash
./SETUP.sh
```

TBD

## Run & Usage

Once the setup step above has been completed, simply run a Cassandra instance by

```bash
./START-CASSANDRA.sh
```

HINT: Test if we can connect to Cassandra with `csql` by

```bash
docker run -it --network n1 --rm cassandra cqlsh c1
```

Start a server manually (e.g. on port 4444)

```bash
node app/main -p 4444
```

### Build & Run from Docker

To build docker, execute

```bash
./BUILD-DOCKER.sh
```

Then run docker container. At this point, it requires Cassandra docker to already runs.

```bash
./RUN-DOCKER.sh
```

To stop after use, run the script:

```bash
./STOP-DOCKER.sh
```

### Query REST API

Query records (via curl) and prettify JSON output

```bash
curl 0.0.0.0:4444/ls/ > jq
```

Add a new record

```bash
curl -X POST "0.0.0.0:4444/add/{id}?v={}"
```

where, `id` represents an id of the new record you want to add. 

## Terminating services

After usage, stop the service by:

```bash
TBD
```

Stop Cassandra docker instance

```bash
./STOP-CASSANDRA.sh
```

## Licence

MIT