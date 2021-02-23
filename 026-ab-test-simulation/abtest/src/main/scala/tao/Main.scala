package tao

import scala.util.Random
import tao.lib._

// Target: Maximise % Increase of CTR
case object CTRExp extends Experiment {
  override val variantA = GaussianRandomHypothesis(
    mean=0.0, variance=0.00125, cap=Some(-0.25, 0.25)
  )
  override val variantB = GaussianRandomHypothesis(
    mean=1.45, variance=0.013, cap=Some(-0.01, 2.00)
  )
  override def measureSample(samples: Seq[Double]): Double = {
    // Just mean
    samples.sum / samples.size.toDouble
  }
}



object Main extends App {
  Console.println("------------------------------")
  Console.println("Measuring CTR from A/B test")
  val ctrValue = CTRExp.evaluateValue(
    confidence=0.95,
    numBins=500)
  Console.println(s"At confidence level = 95%, CTR rate = ${ctrValue.get}")
}