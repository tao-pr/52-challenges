package example

import org.scalatest.funspec.AnyFunSpec
import org.scalatest.matchers.should.Matchers

trait Node { 
  def v: String = "(end)"
  def add(a: Int): Node
}
case object EndNode extends Node {
  override def add(a: Int) = LinkedList(a, EndNode) 
}
case class LinkedList(n: Int, next: Node) extends Node {
  override def v = s"$n : ${next.v}"
  override def add(a: Int) = LinkedList(n, next.add(a))
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
      rv.v shouldBe "4 : 3 : 2 : 1 : (end)"
    }


    it("Take last [n] elements from the linked list"){
      val v = LinkedList(
        1, LinkedList(
          2, LinkedList(
            3, LinkedList(
              4, EndNode))))

      // do it 
      def takeLast(arr: Node, n: Int): Node = {
        recursiveTake(arr, n, EndNode, 0)
      }

      def recursiveTake(arr: Node, n: Int, collected: Node, numCollected: Int): Node = {
        arr match {
          case EndNode => collected
          case LinkedList(a, next) => 
            if (numCollected >= n){
              val newCollected = collected match {
                case EndNode => LinkedList(a, EndNode) // collect as new list
                case LinkedList(k,tail) => // drop head to retain length
                  tail.add(a)
              }
              recursiveTake(next, n, newCollected, numCollected+1 )
            }
            else 
              recursiveTake(next, n, collected.add(a), numCollected+1)
        }
      }

      // test
      takeLast(v, 1).v shouldBe "4 : (end)"
      takeLast(v, 2).v shouldBe "3 : 4 : (end)"
      takeLast(v, 6).v shouldBe "1 : 2 : 3 : 4 : (end)"
    }

  }

}
