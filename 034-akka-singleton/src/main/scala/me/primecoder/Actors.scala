package me.primecoder

import akka.actor.typed.ActorRef
import akka.actor.typed.ActorSystem
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import akka.actor.Actor

import scala.collection.mutable.HashMap

class MutableSingleton extends Actor {
  
  def receive: Actor.Receive = {
    case AddKeySignal =>
      val key = MutableSingleton.data.size+1
      val value = scala.util.Random.nextLong.toString
      Console.println(s"Singleton receiving update signal : $key")
      Console.println(s"... Updating $key -> $value")
      MutableSingleton.data.addOne(key, value)

    case GetKeySignal(key) =>
      Console.println(s"Singleton receiving get signal : $key")
      Console.println(s"... Obtaining $key -> ${MutableSingleton.data.get(key)}")
  }

}

object MutableSingleton extends MutableSingleton {
  private var data = new HashMap[Int, String]
}


