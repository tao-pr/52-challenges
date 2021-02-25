package example

import org.scalatest.funspec.AnyFunSpec
import org.scalatest.matchers.should.Matchers

trait Node { 
  def v: String = "(end)"
  def add(a: Int): LinkedList
  def getNext: Node = EndNode
  def ++(tail: Node): Node
  def insertAt(a: Int, i: Int): LinkedList
}
case object EndNode extends Node {
  override def add(a: Int) = LinkedList(a, EndNode)
  override def ++(tail: Node) = tail match {
    case LinkedList(n, next) => LinkedList(n, next)
    case EndNode => EndNode
  }
  def insertAt(a: Int, i: Int) = add(a)
}
case class LinkedList(n: Int, next: Node) extends Node {
  override def v = s"$n : ${next.v}"
  override def add(a: Int) = LinkedList(n, next.add(a))
  override def getNext = next
  override def ++(tail: Node) = LinkedList(n, next ++ tail)
  override def insertAt(a: Int, i: Int) = {
    if (i<=0){
      LinkedList(a, LinkedList(n, next))
    }
    else {
      LinkedList(n, next.insertAt(a, i-1))
    }
  } 
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


    it("Find middle element of linked list in one pass"){
      val v1 = LinkedList(
        1, LinkedList(
          2, LinkedList(
            3, LinkedList(
              4, LinkedList(
                5, EndNode)))))
      val v2 = LinkedList(
        1, LinkedList(
          2, LinkedList(
            3, LinkedList(
              4, LinkedList(
                5, LinkedList(
                  6, LinkedList(
                    7, EndNode)))))))

      // do it 
      def findMiddle(arr: LinkedList): Int = {
        // step `middle` to the next every even element
        // element 0 -> middle=0
        // element 1 -> middle=0
        // element 2 -> middle=1
        // ..
        var middle: Node = arr
        var a: Node = arr
        var i = 0
        while (a != EndNode){
          if (i>0 && i%2==0){
            // step next
            middle = middle.getNext
          }
          a = a.getNext
          i += 1
        }
        middle match {
          case LinkedList(m, _) => m
          case EndNode => -1 // No middle value found
        }
      }

      // test 
      findMiddle(v1) shouldBe 3
      findMiddle(v2) shouldBe 4
    }


    it("Permutation of linked list"){
      val v1 = LinkedList(
        1, LinkedList(
          2, LinkedList(
            3, EndNode)))

      // do it 
      // 
      // Steinhaus–Johnson–Trotter algorithm
      // wiki: https://en.wikipedia.org/wiki/Steinhaus%E2%80%93Johnson%E2%80%93Trotter_algorithm
      def permute(ns: Node): Seq[Node] = {
        ns match {
          case EndNode => 
            Seq.empty

          case LinkedList(n, EndNode) =>
            Seq(LinkedList(n, EndNode))

          case LinkedList(n, LinkedList(m, EndNode)) =>
            Seq( // Just swap 2 elements
              LinkedList(n, LinkedList(m, EndNode)),
              LinkedList(m, LinkedList(n, EndNode)))

          case LinkedList(n, next) =>
            val permuteOfNext = permute(next)
            // Add [n] to every combination
            permuteOfNext.map{ ps =>
              var curr = ps
              var left: Node = EndNode
              var right: Node = ps
              var ss = Seq.empty[Node]
              while (right != EndNode){
                ss = ss :+ (left.add(n) ++ right)
                right match {
                  case LinkedList(r,rs) => 
                    left = left.add(r)
                    right = rs
                }
              }
              ss = ss :+ ps.add(n)
              ss
            }.reduce(_ ++ _)
        }
      }


      // test
      val w = Seq(
        "1 : 2 : 3 : (end)",
        "1 : 3 : 2 : (end)",
        "2 : 1 : 3 : (end)",
        "2 : 3 : 1 : (end)",
        "3 : 2 : 1 : (end)",
        "3 : 1 : 2 : (end)",
      )
      permute(v1).map(_.v) should contain theSameElementsAs(w)

    }

  }

}
