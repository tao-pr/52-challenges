package com.tao.image

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.ml.image.ImageSchema

import breeze.linalg.Vector

import com.tao.IO

case class Label(filename: String, noise: Double, x: Int, y: Int)

case class LabelledFeature(x: Int, y: Int, features: Array[Float])

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

  def train(images: DataFrame, labels: DataFrame, trainRatio: Double)
  (implicit spark: SparkSession) = {

    import spark.implicits._

    val filename = udf( (s: String) => s.split("/").last )
    val labelledDf = images
      .withColumn("filename", filename(col("image.origin")))
      .join(labels, "filename")

    colourPrint(DEBUG, "[Training]", "Generating feature vectors")
    val features = labelledDf.rdd.map{ row =>
      val labelx = row.getAs[Int]("x")
      val labely = row.getAs[Int]("y")
      val image = row.getAs[Row]("image")
      val imData = ImageSchema.getData(image) // Array[Byte]
      val w = ImageSchema.getWidth(image)
      val h = ImageSchema.getWidth(image)

      // Collect all border pixels
      val buff = scala.collection.mutable.ArrayBuffer.empty[Float]
      (0 to h).foreach{ j =>
        // Collect left border 
        val leftB = imData(j*w*3 + 0)
        val leftG = imData(j*w*3 + 1)
        val leftR = imData(j*w*3 + 2)
        // Collect right border
        val rightB = imData(j*w*3 + (w-1)*3+0)
        val rightG = imData(j*w*3 + (w-1)*3+1)
        val rightR = imData(j*w*3 + (w-1)*3+2)

        buff += (leftB+leftG+leftR)/3.0f
        buff += (rightB+rightG+rightR)/3.0f
      }

      // NOTE: Skip leftmost and rightmost pixels, as they overlap with previous step
      (1 to w-1).foreach{ i =>
        // Collect top border
        val topB = imData(i*3 + 0)
        val topG = imData(i*3 + 1)
        val topR = imData(i*3 + 2)
        // Collect the bottom border
        val bottomB = imData((h-1)*w*3 + i*3 + 0)
        val bottomG = imData((h-1)*w*3 + i*3 + 1)
        val bottomR = imData((h-1)*w*3 + i*3 + 2)

        buff += (topB+topG+topR)/3.0f
        buff += (bottomB+bottomG+bottomR)/3.0f
      }

      LabelledFeature(labelx, labely, buff.toArray)

    }.toDS

    val seq: Array[Dataset[LabelledFeature]] = features.randomSplit(Array(trainRatio, 1-trainRatio))
    val trainDs = seq.head
    val testDs  = seq.last

    colourPrint(DEBUG, "Training set : ", s"${trainDs.count} images")
    colourPrint(DEBUG, "Test set     : ", s"${testDs.count} images")


    // TAOTODO:
  }
}