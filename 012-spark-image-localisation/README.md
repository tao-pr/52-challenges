# Spark Image Localisation

Trying image processing on Spark

[More info: Image support on Spark](https://issues.apache.org/jira/browse/SPARK-21866)

## Submit a job

First, Package a JAR

```bash
$ sbt sil/package
```

Then submit to your favourite cluster via

```bash
$ $SPARK_HOME/bin/spark-submit \
  --class com.tao.Job \
  --master URL \
  --executor-memory 12G \
  --total-executor-cores 50 \
  target/scala-2.12/spark-image-localisation_2.12-0.1.0-SNAPSHOT.jar \
  <ADDITIONAL ARGS>
```

## Local Spark instance

Typical spark path variable:

> $SPARK_HOME=/usr/local/Cellar/apache-spark/2.4.4/libexec

Start a Spark instance by (see the URL on Spark master UI)

```bash
$SPARK_HOME/sbin/start-all.sh
```

The script to stop services is also inside the same directory.

## Licence

BSD
