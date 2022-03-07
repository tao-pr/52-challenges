# Akka Mutable Singleton and Scheduler

Build an Akka project which is planned to run as a background process 
with mutable object. This object is updated periodically with Akka scheduler 
and the background process may read this mutable singleton object at any point in time.

## Project Setup

This project is initialised with following g8 template

```sh
sbt -Dsbt.version=1.3.6 new akka/akka-quickstart-scala.g8
```

## Build and run

Simply

```sh
sbt compile
sbt run # TAOTODO add java parameter to adjust heap size
```

## Licence

MIT

