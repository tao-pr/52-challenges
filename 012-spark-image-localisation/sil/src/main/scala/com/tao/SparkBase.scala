package com.tao

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}

import org.apache.log4j.Level

trait SparkBase {
  val appName: String
  lazy val spark = SparkSession.builder.appName(appName).getOrCreate()

  lazy val logger = {
    val log = org.apache.log4j.LogManager.getLogger(appName)
    log.setLevel(Level.INFO)
    log
  }

  def shutdown(){
    spark.stop()
  }
}