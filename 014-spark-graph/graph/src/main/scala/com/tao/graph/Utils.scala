package com.tao.graph

import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD
import org.apache.spark.graphx.Graph
import org.apache.spark.graphx.{Graph, VertexRDD, Edge}
import org.apache.spark.graphx.VertexId
import scala.collection.immutable.IndexedSeq

object Util {

  // NOTE: RDD[(VertexId, VertexId)] is equivalent to Graph[VD, VertexId]
  def generateEdges(numEdges: Int, numNodes: Int)
  (implicit sc: SparkContext): Graph[String, Long] = {
    val generateEdgeTuple = (index: Int, numNodes: Int) => {
      val Vector(a,b): IndexedSeq[Long] = (0 to 1).map(_ => scala.math.abs(scala.util.Random.nextLong % numNodes.toLong))
      val attr = 0L
      new Edge(a, b, attr)
    }
    val vertices = sc.parallelize((1 to numNodes).map{i => (i.toLong, s"City-$i")})
    val edges    = sc.parallelize((1 to numEdges).map{i => generateEdgeTuple(i, numNodes)})
    Graph(vertices, edges)
  }

}