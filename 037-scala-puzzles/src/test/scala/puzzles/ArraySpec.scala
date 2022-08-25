package puzzles

import org.scalatest.flatspec.AnyFlatSpec

import scala.annotation.tailrec
import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer

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

  it should "cut circular array at max value" in {
    def cut(cc: Array[Int]): Iterable[Int] = {
      var i = 0
      var cand = cc
      var n = cc
      var tail = cc
      while (n.nonEmpty){ // O(L)
        if (cand.head < n.head){
          tail = cand
          cand = n
          i += 1
        }
        n = n.tail
      }

      if (i==0) // first is largest OR empty input
        cc
      else {
        // cut at @i
        cc.slice(i, cc.length) ++ cc.take(i) // O(N)
      }
      // total: O(N) + O(N)
    }

    assert(cut(Array(1,3,5,1,2)) == List(5,1,2,1,3))
    assert(cut(Array(1)) == List(1))
    assert(cut(Array(10,2,3,1)) == List(10,2,3,1))
    assert(cut(Array(5,0,1,2,5,1)) == List(5,0,1,2,5,1))
    assert(cut(Array(1,5)) == List(5,1))
    assert(cut(Array(3,3,3)) == List(3,3,3))
  }

  it should "locate max value in a matrix which sorted within a row" in {
    def max(mat: Array[Array[Int]]): Int = {
      // R x C
      // locate max value of each row
      val max = mat.foldLeft(Int.MinValue){ case (max, row) => // O(R)
        // locate max
        max.max(row.head.max(row.last))
      }
      max
    }

    val m1 = Array(
      Array(1,5,6),
      Array(2,7,7),
      Array(6,3,1)
    )
    assert(max(m1) == 7)

    val m2 = Array(
      Array(1,10),
      Array(2,0),
      Array(3,5),
      Array(0,0)
    )
    assert(max(m2) == 10)

    val m3 = Array(
      Array(0,1,1,5,7),
      Array(1,2,5,7,7),
      Array(2,5,6,6,8),
      Array(10,2,1,1,1)
    )
    assert(max(m3) == 10)

    val m4 = Array(
      Array(0,1,1,2,5),
      Array(3,2,1,1,0),
      Array(6,4,4,2,2),
      Array(4,5,5,5,5)
    )
    assert(max(m4) == 6)
  }

  it should "find gaps of missing values in array" in {
    // eg
    // [1,3,5,6,7,8,9]
    // => [1,1]

    // [0,15,16,19,25,40,41,43]
    // => [14,2,5,14,1]
    def eval(arr: Array[Int]): Array[Int] = {
      var prev = arr.head
      val gap = new mutable.ArrayBuffer[Int]()
      for (a <- arr) { // O(L)
        if (a - prev > 1)
          gap.addOne(a - prev - 1)
        prev = a
      }
      gap.toArray
    }

    assert(eval(Array(1, 3, 5, 6, 7, 8, 9)).toList == List(1, 1))
    assert(eval(Array(0,15,16,19,25,40,41,43)).toList == List(14,2,5,14,1))
    assert(eval(Array(0,1,2,3,4,5,6)).isEmpty)
  }

  it should "remove all ascending elements (more than 2 adjacent) from array" in {
    def eval(arr: List[Int]): List[Int] = {
      if (arr.length <= 2) arr
      else {
        var pre = arr.head
        var i = 0
        val tail = arr.tail.dropWhile{ a =>
          val isAsc = a > pre
          if (isAsc)
            i+=1
          pre = a
          isAsc
        }

        if (i>=2)
          eval(tail)
        else{
          arr.slice(0, i+1) ++ eval(tail)
        }
      }
    }

    assert(eval(List(1,15,19,16,17,2,15)) == List(16,17,2,15))
    assert(eval(List(15,13,12,13,15,12,13,15)) == List(15,13))
    assert(eval(List(1,2,3,40,57)).isEmpty)
  }

  it should "zigzag walk matrix" in {
    def eval(mat: Array[Array[Int]]): Array[Int] = {
      walk(mat, Some(0), None)
    }

    def walk(mat:Array[Array[Int]], beginCol: Option[Int], beginRow: Option[Int]): Array[Int] = {
      (beginCol, beginRow) match {
        case (Some(col), _) =>
          var (i,j) = (0,col)
          val buff = new ArrayBuffer[Int]()
          while (j>=0 && i<=mat.length-1){
            buff.addOne(mat(i)(j))
            i += 1
            j -= 1
          }
          if (col==mat.head.length-1) {
            // end of cols, walk from next row instead
            buff.toArray ++ (if (mat.length>1) walk(mat, None, Some(1)) else Array.empty)
          } else
            buff.toArray ++ walk(mat, Some(col+1), None)

        case (None, Some(row)) =>
          var (i,j) = (row, mat.head.length-1)
          val buf = new ArrayBuffer[Int]()
          while (j>=0 && i<=mat.length-1){
            buf.addOne(mat(i)(j))
            i += 1
            j -= 1
          }
          if (row>=mat.length-1)
            buf.toArray
          else
            buf.toArray ++ walk(mat, None, Some(row+1))

        case _ => Array.empty
      }
    }

    val m1 = Array(
      Array(1,2,3),
      Array(4,5,6),
      Array(7,8,9))
    assert(eval(m1).toList == List(1,2,4,3,5,7,6,8,9))

    val m2 = Array(Array(1))
    assert(eval(m2).toList == List(1))

    val m3 = Array(
      Array(1,2,3,4,5),
      Array(1,2,3,4,5))
    assert(eval(m3).toList == List(1,2,1,3,2,4,3,5,4,5))

    val m4 = Array(
      Array(1,2,3,4,5)
    )
    assert(eval(m4).toList == List(1,2,3,4,5))

    val m5 = Array(
      Array(1),
      Array(2),
      Array(3))
    assert(eval(m5).toList == List(1,2,3))
  }

  it should "find longest subarray in all arrays" in {
    def eval(arr: List[Array[Int]]): List[Int] = {
      val ns = arr.sortBy(_.length).map(_.toBuffer)
      sub(ns.head, ns.tail, Nil, Nil)
    }

    def sub(b: mutable.Buffer[Int], arr: Iterable[mutable.Buffer[Int]], pre: List[Int], longest: List[Int]): List[Int] = {
      if (b.isEmpty) if (longest.length > pre.length) longest else pre
      else {
        val barr = arr.map{_.dropWhile(_ != b.head)}
        if (barr.exists(_.isEmpty)){
          // no match, clear pre & start over
          val ls = if (longest.length > pre.length) longest else pre
          sub(b.tail, arr, Nil, ls)
        }
        else {
          // still match further
          sub(b.tail, barr.map(_.tail), pre :+ b.head, longest)
        }
      }
    }

    assert(eval(
      Array(1,2,3) :: Array(2,3,5,3) :: Array(0,3,3,2,3) :: Nil
    ).toList == List(2,3))
    assert(eval(
      Array(1,1,1,1,1,1,1,1,1) :: Array(0,1,1,5,3,1,1,1) :: Array(1,1,1,5,1,1,1) :: Nil
    ).toList == List(1,1,1))
    assert(eval(
      Array(3) :: Array(1,2,5) :: Array(6,5,7,1,2,5) :: Nil
    ).toList == Nil)
  }

  it should "evaluate vol of trapped rain water" in {
    def eval(cell: Array[Int]): Int = {

      if (cell.isEmpty)
        0
      else {
        val level = cell.head
        var vol = 0
        var maxRight = 0
        val tail = cell.tail.dropWhile{ c =>
          if (c<level){
            vol += level-c
          }
          maxRight = maxRight.max(c)
          c<level
        }

        if (vol==0) { // left most cell is not the wall
          eval(cell.tail)
        }
        else if (tail.isEmpty && vol>0){ // left wall is too high, cannot find higher right wall
          eval(maxRight +: cell.tail)
        }
        else
          vol + eval(tail)
      }
    }


    assert(eval(Array(0,0,0,0)) == 0)
    assert(eval(Array(1,1,1,0,1,1,2,0,1))==2)
    assert(eval(Array(1,0,2,1,0,3,3,4,1,3)) == 1+3+2)
    assert(eval(Array(0,1,3,5,2,1)) == 0)
    assert(eval(Array(3,2,1,2,3,1)) == 1+2+1)
  }

  it should "find matching position of sequence of subarray" in {
    // -1 means wildcard
    def eval(arr: Array[Int], pat: Array[Int], index: Int = 0): Int = {
      if (pat.length > arr.length || arr.isEmpty)
        -1
      else {
        if (pat.lazyZip(arr).exists{ case (p,a) => p!=a && p != -1 })
          eval(arr.tail, pat, index+1)
        else
          index
      }
    }

    assert(eval(Array(1,2,3,4), Array(2,-1)) == 1)
    assert(eval(Array(1,2,3,2,3,5), Array(2,-1,-1)) == 1)
    assert(eval(Array(0,3,5,3,2,5,5,1), Array(-1,5,-1,1)) == 4)
    assert(eval(Array(1,1,3,1), Array(-1,-1)) == 0)
  }

}
