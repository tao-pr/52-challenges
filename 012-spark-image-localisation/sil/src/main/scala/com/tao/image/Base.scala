package com.tao.image

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}

object ImageBase {
  
  def loadData(dirPath: String): DataFrame = ???

  def createModel: AnyRef = ???

  def train(m: AnyRef, data: DataFrame): AnyRef = ???

  def test(m: AnyRef, data: DataFrame): AnyRef = ???
}