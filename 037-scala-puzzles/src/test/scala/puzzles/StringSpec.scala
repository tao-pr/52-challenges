package puzzles

import org.scalatest.flatspec.AnyFlatSpec

import scala.annotation.tailrec
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


  it should "evaluate math expression" in {

    // operators: +,-,*
    // with parenthesis
    case class Exp(var a: Option[Int], var op: Option[Char], var b: Option[Int]){
      def eval : Int = (op match {
        case None => a
        case Some('+') => for (i <- a ; j <- b) yield i+j
        case Some('-') => for (i <- a ; j <- b) yield i-j
        case Some('*') | Some('x') => for (i <- a ; j <- b) yield i*j
      }).getOrElse(a.getOrElse(0))

      def add(t: Char) = {
        if (Set('*','x','+','-').contains(t))
          this.op = Some(t)
        else if (op.isDefined)
          b match {
            case None => this.b = Some(t.toString.toInt)
            case Some(v) => this.b = Some(v * 10 + t.toString.toInt)
          }
        else a match {
          case None => this.a = Some(t.toString.toInt)
          case Some(v) => this.a = Some(v * 10 + t.toString.toInt)
        }
        this
      }

      def addInt(n: Int) = {
        if (a.isEmpty) this.a = Some(n)
        else this.b = Some(n)
      }

    }

    def eval(expr: String): Int = {
      // 1 - look for opening & closing parenthesis
      // 2 - evaluate inside
      ev(expr, Exp(None, None, None))._2
    }

    def ev(expr: String, e: Exp): (String, Int) = {
      if (expr.isEmpty) ("",e.eval)
      else {
        if (expr.startsWith("(")){
          val (remain,sub) = ev(expr.tail, Exp(None, None, None))
          e.addInt(sub)
          ev(remain, e)
        }
        else if (expr.startsWith(")")) {
          (expr.tail, e.eval)
        }
        else {
          ev(expr.tail, e.add(expr.head))
        }
      }
    }


    assert(eval("1+1") == 2)
    assert(eval("3+(10x5)") == 53)
    assert(eval("2+(2-3)") == 1)
    assert(eval("((2+(2-3))*50)+10") == 60)
  }

  it should "find a string that matches all search patterns" in {
    def split(s: String): Seq[String] ={
      if (s.endsWith("*"))
        s.split('*') :+ ""
      else
        s.split('*')
    }

    def max(a: String, b: String) = if (a.length>=b.length) a else b

    def eval(patterns: List[String]): String = {
      val splits = patterns.map(split) // O(P*L)
      var h = "" // head
      var t = "" // tail
      var m = "" // mid
      for (s <- splits){
        h = max(h, s.head)
        if (s.tail.nonEmpty){
          t = max(t, s.tail.last)
          val mid = s.tail.dropRight(1)
          if (mid.nonEmpty){
            m += mid.mkString("")
          }
        }
      }

      h + m + t

      // splits look like:
      // ['',1]
      // [1,'']
      // [123,'']
    }

    assert(eval("*1" :: "1*" :: "123*" :: Nil) == "1231")
    assert(eval("a*b*c*" :: "abc*e" :: "*bk*" :: Nil) == "abcbcbke" )

  }

  it should "find minimum inserts to make a string a palindrome" in {
    def eval(s: String): Int = {
      var w = s
      var num = 0
      while (w.nonEmpty){
        if (w.head != w.last) {
          num += 1
          w = trim(w)
        }
        else w = w.tail.dropRight(1) // trim both sides
      }
      num
    }

    def trim(s: String): String = { // remove odd from a likely palindrome
      // h:mid:l
      if (s.length <= 1)
        s
      else{
        val l = s.last
        val m = s.tail.dropRight(1)
        m match {
          case "" => s.tail // empty middle, doesn't matter which end to drop
          case mm if mm.head == l => s.tail
          case _ => s.dropRight(1)
        }
      }
    }

    assert(eval("aa") == 0)
    assert(eval("abc") == 2) // abc[ba]
    assert(eval("1k13") == 1) // [3]1k13
    assert(eval("*13*") == 1) // *13[1]*
    assert(eval("0001001") == 2) // [1]000100[0]1
    assert(eval("akkaaakka") == 0)
   }
}