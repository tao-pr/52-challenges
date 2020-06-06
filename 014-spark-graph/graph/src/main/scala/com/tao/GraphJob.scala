package com.tao

import org.apache.spark.sql.{Dataset, DataFrame}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.{Column,Row}
import org.apache.spark.sql.catalyst.encoders._
import org.apache.spark.sql.functions._
import org.apache.spark.sql.types._

import org.apache.spark.graphx.PartitionStrategy

import com.tao.graph._

object GraphJob extends App with SparkBase {

  override val appName = "GraphJob"
  override val sparkMaster = "local"

  colourPrint(INFO, "[Job]", "Starting ...")

  implicit val _spark = spark
  implicit val _sc    = spark.sparkContext

  // Generate graph RDDs
  val er = () => {
    val b = scala.util.Random.nextInt
    if (b > 0) DrivingDistance(scala.math.abs(b%100))
    else TrainDistance(scala.math.abs(b%100))
  }
  val graph = Util.generateGraph(numEdges=1000, numNodes=200)
  val graphE = Util.generateGraphWithEdgeAttr(numEdges=1000, numNodes=50, edgeRandomiser=er)

  graph.cache
  graphE.cache

  // Display graph
  colourPrint(INFO, "[graph]", "")
  Util.printGraph(graph)

  // Map vertices & Repartition edges by source vertex
  val graph_ = graphE
    .mapVertices((vertexId, vd) => City(vertexId))
    .partitionBy(PartitionStrategy.EdgePartition1D) // Edges with same source vertex go to the same partition
  colourPrint(INFO, "[graph_] (mapped)", "")
  Util.printGraph(graph_)

  // Aggregate: Count num of outbound edges on each vertex
  val sumDistanceEdges = graph_
    .mapEdges((partitionId, iter) => iter.map(_.attr.toSumDistance))
    .groupEdges(_ + _)
  colourPrint(INFO, "[sumDistanceEdges]", s"${sumDistanceEdges.edges.count} entries")
  Util.printEdges(sumDistanceEdges)

  // Traverse graph

  // Subgraph

  // Save graph

  shutdown
}