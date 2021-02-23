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

private [lib] trait Calculator {
  
  // Sample with replacement
  def draw(outcomes: Seq[Double], num: Int): Seq[Double] = {
    (1 to num).map{_ => outcomes(Random.nextInt(outcomes.length))}
  }

  def toProbDist(values: Seq[Double], numBins: Int): Seq[(Double,Double,Double)] = {
    val min = values.min
    val max = values.max
    val binMarks = (0 to numBins).map{ i => i*(max-min)/numBins + min }
    val binBounds = binMarks.zip(binMarks.tail)
    val prob = binBounds.map{ case (a,b) => 
      val p = values.filter{v => a<=v && v<b}.size.toDouble / values.size
      (a,b,p)
    }
    prob
  }

  def findValueAtSignificance(density: Seq[(Double,Double,Double)], accum: Double, confidence: Double): Option[Double] = {
    if (density.isEmpty)
      None
    else {
      val (a,b,p) = density.head
      val accum_ = accum + p
      if (accum_ >= confidence){
        // Found it
        Some(a)
      }
      else 
        findValueAtSignificance(density.tail, accum_, confidence)
    }
  }
}

trait Experiment extends Calculator {
  val variantA: Hypothesis
  val variantB: Hypothesis

  // Measure a value from sample
  def measureSample(samples: Seq[Double]): Double

  def evaluateValue(
    confidence: Double = 0.95,
    numSamples: Int=5000,
    sampleSize: Int=100,
    numBins: Int=1000): Option[Double] = {

    // Generate outcomes (mixed variants)
    val outcomesA = variantA.generateOutcome(numSamples)
    val outcomesB = variantB.generateOutcome(numSamples)

    val outcomes = outcomesA.zip(outcomesB).map{ case(a,b) => b-a }

    // Draw from samples
    val samples = (1 to numSamples).map{_ => draw(outcomes, sampleSize) }

    // Measure sample values
    val values = samples.map(measureSample)

    // Generate probability distribution
    val probDist = toProbDist(values, numBins)

    var accumDensity: Double = 0
    findValueAtSignificance(probDist, accumDensity, confidence)
  }
}


