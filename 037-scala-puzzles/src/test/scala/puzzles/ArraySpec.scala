package puzzles

import org.scalatest.flatspec.AnyFlatSpec

import scala.annotation.tailrec

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
}
