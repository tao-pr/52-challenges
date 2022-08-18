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

}