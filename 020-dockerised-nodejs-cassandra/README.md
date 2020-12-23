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