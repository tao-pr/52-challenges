package example

import org.scalatest.funspec.AnyFunSpec
import org.scalatest.matchers.should.Matchers

class HelloSpec extends AnyFunSpec with Matchers {
  
  describe("Single array puzzles"){

    it("Remove duplicates and sort array: O(N)"){
      val v = Seq(1,15,3,2,1,1,3,15,6,5,3,1,5,3,15)
      val w = v.toSet.toList.sorted

      // do it
      def addByOrder(vec: Seq[Int], a: Int): Seq[Int] = {
        if (vec.isEmpty || a < vec.head){
          a +: vec
        }
        else if (a > vec.head){
          vec.head +: addByOrder(vec.tail, a)
        }
        else vec // Never add element it already has
      }

      var v_ = Seq.empty[Int]
      for (n <- v){
        v_ = addByOrder(v_, n)
      }

      // test
      v_ should contain theSameElementsInOrderAs (w)
    }
  }

}
