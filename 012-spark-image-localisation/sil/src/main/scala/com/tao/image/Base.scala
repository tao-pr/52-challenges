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

    // Feature ideas:
    // - Mean horizontal vector
    // - Mean vertical vector
    val features = labelledDf.rdd.map{ row =>
      val labelx = row.getAs[Int]("x")
      val labely = row.getAs[Int]("y")
      val image  = row.getAs[Row]("image")
      val imData = ImageSchema.getData(image) // Array[Byte]
      val w = ImageSchema.getWidth(image)
      val h = ImageSchema.getWidth(image)
      
      // Mean horizontal vector
      val hvector = scala.collection.mutable.ArrayBuffer.empty[Float]
      (0 until h).foreach{ j =>
        if (hvector.size==0){
          (0 until w).foreach{ i =>
            hvector += imData(j*w+i).toFloat
          }
        }
        else {
          (0 until w).foreach{ i =>
            hvector(i) += imData(j*w+i).toFloat
          }
        }
      }

      // Mean vertical vector
      val vvector = scala.collection.mutable.ArrayBuffer.empty[Float]
      (0 until h).foreach{ i =>
        if (vvector.size==0){
          (0 until h).foreach{ j =>
            vvector += imData(j*w+i).toFloat
          }
        }
        else {
          (0 until h).foreach{ j =>
            vvector(j) += imData(j*w+i).toFloat
          }
        }
      }

      // Calculate mean
      (0 until h).foreach( j => vvector(j) /= w.toFloat )
      (0 until w).foreach( i => hvector(i) /= h.toFloat )

      // Make up feature vector
      vvector ++= hvector
      LabelledFeature(labelx, labely, vvector.toArray)
    }.toDS

    // val features = labelledDf.rdd.map{ row =>
    //   val labelx = row.getAs[Int]("x")
    //   val labely = row.getAs[Int]("y")
    //   val image = row.getAs[Row]("image")
    //   val imData = ImageSchema.getData(image) // Array[Byte]
    //   val w = ImageSchema.getWidth(image)
    //   val h = ImageSchema.getWidth(image)

    //   // Collect all border pixels
    //   val buff = scala.collection.mutable.ArrayBuffer.empty[Float]
    //   (0 to h-1).foreach{ j =>
    //     // Collect left and right border 
    //     val leftPixel  = imData(j*w)
    //     val rightPixel = imData(j*w + (w-1))
    //     buff += leftPixel.toFloat
    //     buff += rightPixel.toFloat
    //   }

    //   // NOTE: Skip leftmost and rightmost pixels, as they overlap with previous step
    //   (1 to w-2).foreach{ i =>
    //     // Collect top and bottom border
    //     val topPixl     = imData(i + 0)
    //     val bottomPixel = imData((h-1)*w + i + 0)

    //     buff += topPixl.toFloat
    //     buff += bottomPixel.toFloat
    //   }

    //   // Normalise the feature vector
    //   val vector = buff.map{_ / buff.sum.toFloat}

    //   LabelledFeature(labelx, labely, buff.toArray)

    // }.toDS

    val seq: Array[Dataset[LabelledFeature]] = features.randomSplit(Array(trainRatio, 1-trainRatio))
    val trainDs = seq.head
    val testDs  = seq.last

    colourPrint(DEBUG, "Training set : ", s"${trainDs.count} images")
    colourPrint(DEBUG, "Test set     : ", s"${testDs.count} images")

    // Create and train a linear model
    // TAOTODO:
  }
}