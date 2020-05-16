package com.tao

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}
import org.apache.spark.sql.catalyst.encoders._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import com.tao.image.ImageBase
import com.tao.IO._

object Job extends App with SparkBase with ImageBase {

  override val appName = "SIL"
  override val sparkMaster = "local"

  colourPrint(INFO, "[Job]", "Starting ...")

  implicit val _spark = spark

  // Prepare the image directory structure as
  // {label}
  //  |-- {file}
  // 
  // So when reading with Spark, the {label} dir becomes another column
  val labels = loadLabels("../011-tensor/data/dataset.csv")
  val images = loadData("../011-tensor/data/*.jpg")
  val model = train(images, labels, trainRatio=0.75)

  // TAOTODO
  


  shutdown
}