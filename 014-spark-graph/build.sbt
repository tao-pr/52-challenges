name := "spark-graph"
organization := "tao"
licenses := Seq("Apache 2.0 License" -> url("http://www.apache.org/licenses/LICENSE-2.0.html"))

val sparkVersion      = "2.4.4"
val scalatest         = "3.0.3"
val scalaLogVersion   = "3.9.2"
val logbackVersion    = "1.1.2"
val circeVersion      = "0.11.1"
val kafkaVersion      = "2.1.0"
val avro4sVersion     = "3.0.4"
scalaVersion         := "2.12.0"

mainClass in (Compile, run) := Some("com.tao.GraphJob")

// Compatibility NOTE: 
// https://docs.scala-lang.org/overviews/jdk-compatibility/overview.html#jdk-12-compatibility-notes

// Circe
libraryDependencies ++= List(
  "io.circe" %% "circe-core",
  "io.circe" %% "circe-generic",
  "io.circe" %% "circe-parser"
).map(_ % circeVersion)

// Test
val devDependencies = List(
  "org.scalatest" %% "scalatest" % "3.0.8" % "test"
)

// Spark
// NOTE: "provided" is supposed to be activated for cluster deployment mode
val sparkDependencies = List(
  "org.apache.spark" %% "spark-core" % sparkVersion,// % "provided",
  "org.apache.spark" %% "spark-sql"  % sparkVersion,// % "provided",
  "org.apache.spark" %% "spark-mllib"  % sparkVersion,// % "provided",
  "org.apache.spark" %% "spark-avro" % sparkVersion// % "provided"
)

lazy val graph = project
  .settings(name := "graph")
  .settings(libraryDependencies ++= sparkDependencies ++ devDependencies)
