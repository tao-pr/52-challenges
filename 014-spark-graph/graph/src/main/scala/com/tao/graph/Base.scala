package com.tao.graph

import org.apache.spark.graphx.Graph
import org.apache.spark.graphx.{Graph, VertexRDD, EdgeRDD}

// Graph representation

class Distance
case class TrainDistance(d: Double) extends Distance 
case class DrivingDistance(d: Double) extends Distance

case class City(id: Long)
