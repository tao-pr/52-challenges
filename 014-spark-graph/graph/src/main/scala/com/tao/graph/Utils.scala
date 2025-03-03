package com.tao.graph

import scala.reflect._

import org.apache.spark.SparkContext
import org.apache.spark.rdd.RDD
import org.apache.spark.graphx.Graph
import org.apache.spark.graphx.{Graph, VertexRDD, Edge}
import org.apache.spark.graphx.VertexId
import scala.collection.immutable.IndexedSeq

object Util {

  // NOTE: RDD[(VertexId, VertexId)] is equivalent to Graph[VD, VertexId]
  def generateGraph(numEdges: Int, numNodes: Int)
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

  def generateGraphWithEdgeAttr[A: ClassTag](numEdges: Int, numNodes: Int, edgeRandomiser: () => A)
  (implicit sc: SparkContext): Graph[String, A] = {
    val generateEdgeTuple = (index: Int, numNodes: Int) => {
      val Vector(a,b): IndexedSeq[Long] = (0 to 1).map(_ => scala.math.abs(scala.util.Random.nextLong % numNodes.toLong))
      new Edge(a, b, edgeRandomiser())
    }
    val vertices = sc.parallelize((1 to numNodes).map{i => (i.toLong, s"City-$i")})
    val edges    = sc.parallelize((1 to numEdges).map{i => generateEdgeTuple(i, numNodes)})
    Graph(vertices, edges)
  }

  def printGraph(g: Graph[_,_]) {
    g.vertices.foreach(n => Console.println(s"NODE => ${n}"))
  }

  def printEdges(g: Graph[_,_]) {
    g.edges.foreach(e => Console.println(s"EDGE => ${e}"))
  }

}