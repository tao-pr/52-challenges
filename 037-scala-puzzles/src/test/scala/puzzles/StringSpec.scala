package puzzles

import org.scalatest.flatspec.AnyFlatSpec

import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

class StringSpec extends AnyFlatSpec {

  it should "identify longest repeated substring" in {
    def sub(s: String): String = {
      val occ = new mutable.HashSet[String]()
      var longest = ""

      val track = new ArrayBuffer[String]() // longest first

      for (c <- s){
        if (longest.size < 1){
          longest = c.toString
        }
        else{
          for (t <- track){
            val pad = t + c
            if (pad.length > longest.length && occ.contains(pad)){
              // new longest found
              longest = pad
            }

            // add to occ always
            occ.addOne(pad)
          }

          // track next
          if (track.nonEmpty) {
            for (i <- 0 until track.length)
              track(i) += c // pad all old trackings
          }
          track.addOne(c.toString) // new track will begin from current char
        }
      }
      longest
    }

    /*
     track (by iter)
     [j]
     ja,[a]
     jaj,aj,[j]
     ...




     */

    assert(sub("jajaja") == "aja")
    assert(sub("a") == "a")
    assert(sub("ajajaaja") == "aja")
    assert(sub("monmonmnonmnon") == "onmnon")
    assert(sub("ssssssssssssss") == "ssssssssssss")
  }



}
