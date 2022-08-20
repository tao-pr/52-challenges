package puzzles

import org.scalatest.flatspec.AnyFlatSpec
import scala.collection.mutable

class NumberTest extends AnyFlatSpec {

  it should "expand prime factorisation of a number" in {

    val knownPrimes = Seq(2,3,5,7,11,13,17,19,23,29)

    def eval(N: Int): Set[Int] = {
      // test with known primes first
      val primes = knownPrimes.filter(_ <= N)
      prune(N, primes)
    }

    def prune(N: Int, primes: Seq[Int]): Set[Int] = {
      if (primes.nonEmpty){
        // test with known primes
        if (N<=1) Set.empty[Int]
        else if (N % primes.last == 0) {
          var M = N
          while (M % primes.last == 0)
            M = M / primes.last
          Set(primes.last) ++ prune(M, primes.dropRight(1))
        }
        else {
          prune(N, primes.dropRight(1))
        }
      }
      else {
        if (N>2)
          // prime sieve
          sieve(N, N-1)
        else
          Set.empty
      }

    }

    def sieve(N: Int, d: Int): Set[Int] = {
      if (d<=1) Set(N)
      else {
        if (N % d == 0)
          sieve(N/d, N/d-1) ++ sieve(d, d-1)
        else{
          sieve(N, d-1)
        }
      }
    }

    assert(eval(2) == Set(2))
    assert(eval(15) == Set(3,5))
    assert(eval(49) == Set(7))
    assert(eval(28) == Set(2,7))
    assert(eval(6662) == Set(2,3331))
    assert(eval(5418) == Set(2,3,7,43))
    assert(eval(264407) == Set(11,13,43))
  }
}
