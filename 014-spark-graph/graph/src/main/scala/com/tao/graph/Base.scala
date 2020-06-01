package com.tao.graph

import org.apache.spark.graphx.Graph

// Graph representation

object MetroGraph {

  case class Station(name: String, cityName: String)

  type Metro = Graph[Station, Double]

}

