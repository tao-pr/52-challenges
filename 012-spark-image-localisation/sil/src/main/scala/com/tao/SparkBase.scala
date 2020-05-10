package com.tao

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}
import org.apache.spark.sql.{SQLContext, SaveMode}
import org.apache.spark.{SparkContext}

object IO extends IO
trait IO {

  trait Level
  case object INFO extends Level
  case object DEBUG extends Level

  def colourPrint(level: Level, title: String, body: String){
    val titleColor = level match {
      case INFO => Console.MAGENTA
      case DEBUG => Console.GREEN
    }
    Console.println(titleColor + title + Console.RESET + Console.CYAN + body + Console.RESET)
  }
}

trait SparkBase extends IO {

  val appName: String
  val sparkMaster: String
  lazy val spark = SparkSession
    .builder.master(sparkMaster)
    .appName(appName)
    .getOrCreate()

  def shutdown(){
    colourPrint(INFO, "[SparkBase]", "Shutting down")
    spark.stop()
  }
}