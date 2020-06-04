package com.tao

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}
import org.apache.spark.sql.catalyst.encoders._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import com.tao.graph._

object GraphJob extends App with SparkBase {

  override val appName = "GraphJob"
  override val sparkMaster = "local"

  colourPrint(INFO, "[Job]", "Starting ...")

  implicit val _spark = spark

  // Generate graph RDDs

  // Map graph 

  // Aggregate graph 

  // Traverse graph

  // Save graph

  ???

  shutdown
}