package com.tao.image

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

import com.tao.IO

case class Label(filename: String, noise: Double, x: Int, y: Int)

trait ImageBase extends IO {

  import IO._
  
  def loadData(dirPath: String)(implicit spark: SparkSession): DataFrame = {
    colourPrint(INFO, "[ImageBase]", s"Loading images from ${dirPath}")
    val dfImages = spark.read.format("image").load(dirPath)
    colourPrint(DEBUG, "... ", s"${dfImages.count} images loaded")
    dfImages.printSchema
    dfImages.select("image.width","image.height","image.origin").show(5, false)
    dfImages
  }

  def loadLabels(labelPath: String)(implicit spark: SparkSession): DataFrame = {
     // |-- filename: string (nullable = true)
     // |-- noise: double (nullable = true)
     // |-- x: integer (nullable = true)
     // |-- y: integer (nullable = true)
    colourPrint(INFO, "[ImageBase]", s"Loading label file from ${labelPath}")
    val labels = spark
        .read
        .option("header", "true")
        .option("inferSchema", "true")
        .option("delimiter", ",")
        .csv(labelPath)
    colourPrint(DEBUG, "... ", s"${labels.count} labels loaded")
    labels.printSchema
    labels.show(5, false)
    labels
  }

  def train(images: DataFrame, labels: DataFrame, trainRatio: Double) = {
    val filename = udf( (s: String) => s.split("/").last )
    val labelledDf = images
      .withColumn("filename", filename(col("image.origin")))
      .join(labels, "filename")

    val Seq(trainDf, testDf) = labelledDf.randomSplit(Seq(trainRatio, 1-trainRatio))


    // TAOTODO:
  }
}