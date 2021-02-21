package tao.lib

import scala.util.Random
import scala.math

trait Hypothesis {
  def generateOutcome(num: Int): Seq[Double]
}

case class GaussianRandomHypothesis(
  mean: Double, 
  variance: Double, 
  cap: Option[(Double,Double)]) extends Hypothesis {
  override def generateOutcome(num: Int) = {
    (1 to num).map{_ => 
      val v = Random.nextGaussian() * math.sqrt(variance) + mean
      cap match {
        case None => v
        case Some((a,b)) => math.min(math.max(v, a), b)
      }
    }
  }
}

case class UniformRandomHypothesis(
  cap: (Double,Double)) extends Hypothesis {
  override def generateOutcome(num: Int) = {
    val (min, max) = cap
    (1 to num).map{_ => Random.nextDouble() * (max-min) + min}
  }
}


