package example

import org.scalatest.funspec.AnyFunSpec
import org.scalatest.matchers.should.Matchers

trait Node { def v: String = "(end)"}
case object EndNode extends Node
case class LinkedList(n: Int, next: Node) extends Node {
  override def v = s"$n : ${next.v}"
}

class HelloSpec extends AnyFunSpec with Matchers {
  
  describe("Single array puzzles"){

    it("Remove duplicates and sort array: O(N^2)"){
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
      for (n <- v){ // always O(N)
        v_ = addByOrder(v_, n) // worst case :O(N)
      }

      // test
      v_ should contain theSameElementsInOrderAs (w)
    }


    it("Reverse a linked list"){
      val v = LinkedList(
        1, LinkedList(
          2, LinkedList(
            3, LinkedList(
              4, EndNode))))
      val w = "4 : 3 : 2 : 1 : (end)"

      // do it 

      // Copy element from [curr] to [target] "in reverse"
      def copyReverseTo(curr: Node, target: Node): Node = curr match {
        case EndNode => // No more node to copy
          target
        case LinkedList(n, next) =>
          copyReverseTo(next, LinkedList(n, target))
      }
      val rv = copyReverseTo(v, EndNode)

      // test
      rv.v shouldBe w
    }



  }

}
