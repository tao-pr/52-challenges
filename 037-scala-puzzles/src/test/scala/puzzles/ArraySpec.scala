package puzzles

import org.scalatest.flatspec.AnyFlatSpec

import java.util
import scala.annotation.tailrec
import scala.collection.mutable.{ArrayBuffer, ListBuffer}

class ArraySpec extends AnyFlatSpec {

  it should "locate all subarrays" in {
    def locate(arr: List[Int], subs: List[List[Int]]): List[Option[Int]] = {
      subs.map(locateSub(arr, _, 0))
    }

    @tailrec
    def locateSub(arr: List[Int], sub: List[Int], i: Int): Option[Int] = {
      if (sub.length>arr.length) None
      else {
        // slide [sub] on [arr] until we find first match
        val N = sub.size
        val tarr = arr.dropWhile(_ != sub.head)
        if (tarr.size < sub.size) None
        else {
          val shift = arr.length - tarr.length
          if (tarr.take(N) == sub)
            Some(i+shift)
          else
            locateSub(tarr.tail, sub, i+shift+1)
        }
      }
    }

    assert(locate(List(1,2,3,4,5), List(1,2) :: List(4,5) :: Nil) == List(Some(0), Some(3)))
    assert(locate(List(1), List(1,2,3) :: Nil) == List(None))
    assert(locate(List(0,0,0,1,2,0), List(0,0,0,0) :: List(0,1,2) :: List(1,2,0,0) :: Nil) == List(None, Some(2), None))
  }

  it should "find deepest descent" in {
    def deepest(arr: List[Int]): Int = {
      if (arr.size <= 1) 0
      else dp(arr.tail, arr.head, arr.head, 0)
    }

    @tailrec
    def dp(arr: List[Int], peak: Int, lowest: Int, record: Int): Int = {
      arr match {
        case Nil => record
        case a::as =>
          if (a > lowest) // end of descent
            dp(as, a, a, record.max(peak-lowest))
          else
            dp(as, peak, a, record.max(peak-a))
      }
    }

    assert(deepest(Nil) == 0)
    assert(deepest(1::2::3::3::2::2::Nil) ==1)
    assert(deepest(0::15::12::3::4::3::0::Nil) == 12)
    assert(deepest(12::9::12::7::4::2::2::4::1::Nil) == 10)
    assert(deepest(1::1::1::2::2::3::Nil) == 0)
  }

  it should "merge N sorted list together" in {
    def merge(ns: List[Int]*): List[Int] = {
      val all = new ArrayBuffer[List[Int]]
      all.addAll(ns) // O(N)
      val buff = new ArrayBuffer[Int]()
      // O(max(L))
      while (all.nonEmpty){
        var min: Option[Int] = None
        var index: Option[Int] = None
        var i = 0
        while (i < all.length){
          if (all(i).isEmpty)
            all.remove(i)
          else {
            if (min.isEmpty || min.exists(_ > all(i).head)){
              min = Some(all(i).head)
              index = Some(i)
            }
            i += 1
          }
        }

        (min, index) match {
          case (Some(m), Some(k)) =>
            buff.addOne(m)
            if (all(k).length > 1)
              all(k) = all(k).tail
            else
              all.remove(k)

          case _ => all.empty
        }
      }

      buff.toList
    }

    assert(merge(List(1), List(1,5,15), List(2,3,6)) == List(1,1,2,3,5,6,15))
    assert(merge(List(0,10), List(2,5), List(3,7,11)) == List(0,2,3,5,7,10,11))
    assert(merge(List.empty, List(1,10)) == List(1,10))
    assert(merge(List(8), List(7), List(6)) == List(6,7,8))
    assert(merge(List.empty, List.empty) == List.empty)
  }
}
