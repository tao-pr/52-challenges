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

  it should "translate word (0-999) into number" in {
    val digit = Seq("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    val map = Map(
      "ten" -> 10,
      "twenty" -> 20,
      "thirty" -> 30,
      "fifty" -> 50,
      "eleven" -> 11,
      "twelve" -> 12,
      "thirteen" -> 13,
      "hundred" -> 100
    ) ++ digit.zipWithIndex.map{ case (d,i) => d -> i }.toMap

    def eval(w: String): Int = {
      tran(w.split(" ").toList) // O(L)
    }

    def tran(w: List[String]): Int = {
      if (w.isEmpty) 0
      else w match {
        case d::Nil => map(d)
        case d::ds =>
          val (v,next) = map.get(d)
            .map{ k => if (ds.head == "hundred") (k*100,ds.tail) else (k,ds) }
            .getOrElse{
              if (d.endsWith("teen"))
                (map(d.dropRight(4))+10, ds)
              else if (d.endsWith("ty"))
                (map(d.dropRight(2))*10, ds)
              else
                (0,ds)
            }
          v + tran(next)
      }
    }

    assert(eval("zero") == 0)
    assert(eval("hundred thirteen") == 113)
    assert(eval("five hundred fifty nine") == 559)
    assert(eval("seventy five") == 75)
  }

  it should "do pattern matching" in {
    /**
     * defines:
     *   *  = any letters (at least 1 letter)
     *   [] = optional pattern
     */
    def eval(paths: Iterable[String], pattern: String): Iterable[String] = {
      paths.filter(matchMe(pattern, _))
    }

    def matchMe(pattern: String, str: String): Boolean = {
      (pattern, str) match {
        case ("", _) => str.isEmpty
        case (_, "") => false
        case ("*",_) => true
        case (p,s) =>
          if (p.head==s.head) matchMe(p.tail, s.tail)
          else if (p.head=='*'){
            // locate next part of string which matches [p.tail]
            var tail = s.tail // leave at least 1 head to match with *
            var tailMatch = false
            while (tail.nonEmpty && !tailMatch){
              tailMatch = matchMe(p.tail, tail)
              tail = tail.tail
            }
            tailMatch
          }
          else if (p.head=='['){
            // locate next part of string which matches [p.tail]
            val subpattern = p.tail.takeWhile(_ != ']')
            val tailPattern = p.tail.dropWhile(_ != ']').tail // of course still optimisable along with line above
            var i = 0 // where to cut for tail pattern match
            var tail = s
            var tailMatch = tailPattern.isEmpty
            while (tail.nonEmpty && !tailMatch){
              tailMatch = matchMe(tailPattern, tail)
              tail = tail.tail
              if (!tailMatch)
                i += 1
            }
            val substr = s.slice(0, i) // [] allows substr to be empty
            tailMatch && (substr.isEmpty || matchMe(subpattern, substr))
          }
          else false
      }
    }

    val p1 = "ab" :: "abc" :: "abbc" :: "abbccc" :: Nil
    assert(eval(p1, "abc")==List("abc"))

    val p2 = "ab" :: "cab" :: "zzab" :: "ppb" :: "paazb" :: Nil
    assert(eval(p2, "*ab") == List("cab", "zzab"))

    val p3 = "pp" :: "ppe1" :: "e" :: "eep" :: "ppee3" :: Nil
    assert(eval(p3, "[pp]e*") == List("ppe1", "eep", "ppee3"))

    val p4 = "kb5" :: "kkb3" :: "kckbk" :: "ak3kb3" :: "kbkb" :: "kbkbk" :: "kbkbkp" :: Nil
    assert(eval(p4, "[k*]kb*") == List("kb5", "kckbk", "kbkb", "kbkbk", "kbkbkp"))
  }

  it should "create a minimum character replace map in string which makes a string a complete palindrome" in {
    def eval(str: String): Map[Char,Char] = {
      // count occurence : O(N)
      val occ = new mutable.HashMap[Char,Int]
      str.foreach{ c => 
        if (occ.contains(c))
          occ(c) += 1
        else occ.addOne(c -> 1)
      }

      val dontReplace = new mutable.HashSet[Char]
      val map = new mutable.HashMap[Char,Char]
      var (l,r) = (0,str.length-1)

      // O(N)
      while (l < r){
        if (str(l) == str(r))
          dontReplace.addOne(str(l))
        else {
          // replace one
          if (dontReplace.contains(str(l)) || occ(str(r)) < occ(str(l))){
            // replace right
            map.addOne(str(r) -> str(l))
            dontReplace.addOne(str(l))
          }
          else {
            //replace left
            map.addOne(str(l) -> str(r))
            dontReplace.addOne(str(r))
          }
        }
        l +=1
        r -=1
      }

      map.toMap
    } 

    assert(eval("aaa") == Map.empty)
    assert(eval("aba") == Map.empty)
    assert(eval("aabb") == Map('a' -> 'b'))
    assert(eval("abaa") == Map('b' -> 'a'))
    assert(eval("acbba") == Map('c' -> 'b'))
    assert(eval("acapkak") == Map('k' -> 'a', 'c' -> 'a'))
  }
}