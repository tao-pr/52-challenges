package com.tao.graph

import org.apache.spark.graphx.Graph
import org.apache.spark.graphx.{Graph, VertexRDD, EdgeRDD}

// Graph representation

abstract class Distance { def toSumDistance: SumDistance }
case class TrainDistance(d: Double) extends Distance {
  def toSumDistance = SumDistance(d, 0, 1)
}
case class DrivingDistance(d: Double) extends Distance {
  def toSumDistance = SumDistance(0, d, 1)
}

case class City(id: Long)

case class SumDistance(
  sumTrainDistance: Double, 
  sumDrivingDistance: Double, 
  num: Int) {
  def +(another: SumDistance) = SumDistance(
    sumTrainDistance + another.sumTrainDistance,
    sumDrivingDistance + another.sumTrainDistance,
    num + another.num
  )
}
