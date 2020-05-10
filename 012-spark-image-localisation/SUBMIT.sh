#!/bin/bash

# Submit JAR locally
sbt sil/package
$SPARK_HOME/bin/spark-submit \
  --class com.tao.Job \
  --master local \
  --executor-memory 8G \
  --total-executor-cores 1 \
  target/scala-2.12/spark-image-localisation_2.12-0.1.0-SNAPSHOT.jar