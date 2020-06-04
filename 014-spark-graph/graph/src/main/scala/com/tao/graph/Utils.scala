package com.tao.graph

import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD
import org.apache.spark.graphx.Graph
import org.apache.spark.graphx.{Graph, VertexRDD, Edge}
import org.apache.spark.graphx.VertexId

object Util {

  // NOTE: RDD[(VertexId, VertexId)] is equivalent to Graph[VD, VertexId]
  def generateEdges(numEdges: Int, numNodes: Int)
  (implicit sc: SparkContext): Graph[String, VertexId] = {
    val generateEdgeTuple = (index: Int, numNodes: Int) => {
      val Vector(a,b) = (0 to 1).map(_ => scala.math.abs(scala.util.Random.nextLong % numNodes.toLong))
      Edge(a, b)
    }
    val vertices = sc.parallelize((1 to numNodes).map{i => (i.toLong, s"City-$i")})
    val edges    = sc.parallelize((1 to numEdges).map{i => generateEdgeTuple(i, numNodes)})
    Graph(vertices, edges)
  }

}