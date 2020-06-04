package com.tao.graph

import org.apache.spark.graphx.Graph
import org.apache.spark.graphx.{Graph, VertexRDD, EdgeRDD}

// Graph representation

class Node
case object UndefinedNode extends Node
case class City(name: String, size: Long) extends Node
case class Station(name: String) extends Node
