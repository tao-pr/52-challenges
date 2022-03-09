# Akka Mutable Singleton and Scheduler

> But with heavy duty

Build an Akka project which is planned to run as a background process 
with mutable object. This object is updated periodically with Akka scheduler 
and the background process may read this mutable singleton object at any point in time.

## Difference added to 034 challenge

- Mutable map is growing faster and a lot large, aka more than 1 million keys
- Heavy access concurrently
- More than 1 Akka schedules running

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

