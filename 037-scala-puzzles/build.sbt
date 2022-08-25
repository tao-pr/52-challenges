ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.13.8"

val scalaTestVersion = "3.2.11"
val scalaTest = "org.scalatest" %% "scalatest" % scalaTestVersion % "test"

lazy val root = (project in file("."))
  .settings(
    name := "037-scala-puzzles",
    libraryDependencies ++= Seq(scalaTest)
  )
