package com.tao.image

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

import org.apache.spark.ml.linalg.{Vector, DenseVector}
import org.apache.spark.ml.image.ImageSchema
import org.apache.spark.ml.regression.LinearRegression
import org.apache.spark.ml.evaluation.RegressionEvaluator
import org.apache.spark.ml.tuning.TrainValidationSplit

import breeze.linalg.{Vector => BreezeVector}

import com.tao.IO

case class Label(filename: String, noise: Double, x: Int, y: Int)

case class LabelledFeature(filename: String, x: Int, y: Int, featuresX: Vector, featuresY: Vector)

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
      val filename = row.getAs[String]("filename")
      val labelx = row.getAs[Int]("x")
      val labely = row.getAs[Int]("y")
      val image  = row.getAs[Row]("image")
      val imData = ImageSchema.getData(image) // Array[Byte]
      val w = ImageSchema.getWidth(image)
      val h = ImageSchema.getWidth(image)

      // Mean horizontal vector
      val hvector = scala.collection.mutable.ArrayBuffer.empty[Double]
      (0 until h).foreach{ j =>
        if (hvector.size==0){
          (0 until w).foreach{ i =>
            hvector += imData(j*w+i).toDouble
          }
        }
        else {
          (0 until w).foreach{ i =>
            hvector(i) += imData(j*w+i).toDouble
          }
        }
      }

      // Mean vertical vector
      val vvector = scala.collection.mutable.ArrayBuffer.empty[Double]
      (0 until h).foreach{ i =>
        if (vvector.size==0){
          (0 until h).foreach{ j =>
            vvector += imData(j*w+i).toDouble
          }
        }
        else {
          (0 until h).foreach{ j =>
            vvector(j) += imData(j*w+i).toDouble
          }
        }
      }

      // Calculate mean
      (0 until h).foreach( j => vvector(j) /= w.toDouble )
      (0 until w).foreach( i => hvector(i) /= h.toDouble )

      // Make up feature vectors
      LabelledFeature(
        filename, 
        labelx, labely, 
        new DenseVector(hvector.toArray), new DenseVector(vvector.toArray))
    }.toDS

    val seq: Array[Dataset[LabelledFeature]] = features.randomSplit(Array(trainRatio, 1-trainRatio))
    val trainDs = seq.head
    val testDs  = seq.last

    colourPrint(DEBUG, "Training set : ", s"${trainDs.count} images")
    colourPrint(DEBUG, "Test set     : ", s"${testDs.count} images")
    trainDs.printSchema

    // Create and train linear model
    val lgX = new LinearRegression()
      .setFeaturesCol("featuresX")
      .setLabelCol("x")
      .setPredictionCol("pred_x")
      .setElasticNetParam(0.05)
      .setMaxIter(15)
    
    val lgY = new LinearRegression()
      .setFeaturesCol("featuresY")
      .setLabelCol("y")
      .setPredictionCol("pred_y")
      .setElasticNetParam(0.05)
      .setMaxIter(15)

    colourPrint(INFO, "[Training] ", "Starting ...")
    val modelX = lgX.fit(trainDs)
    val modelY = lgY.fit(trainDs)

    colourPrint(INFO, "[Validation] ", "Starting ...")
    val predictionX = modelX.transform(testDs).withColumn("error_x", abs('pred_x - 'x))
    val predictionY = modelY.transform(testDs).withColumn("error_y", abs('pred_y - 'y))
    val prediction = predictionX
      .join(predictionY, "filename")
      .withColumn("error", sqrt(pow('error_x, 2.0) + pow('error_y, 2.0)))

    colourPrint(INFO, "[Validation] ", "Prediction RMSE error : ")
    prediction
      .select(
        (sum('error)/lit(prediction.count.toDouble)).as("sum_error"),
        (sum('error_x)/lit(prediction.count.toDouble)).as("sum_error_x"),
        (sum('error_y)/lit(prediction.count.toDouble)).as("sum_error_y"))
      .show(1, false)

    // +------------------+-----------------+-----------------+
    // |sum_error         |sum_error_x      |sum_error_y      |
    // +------------------+-----------------+-----------------+
    // |100.54706683701589|64.60088423647127|66.33227611133337|
    // +------------------+-----------------+-----------------+
  }
}