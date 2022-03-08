package me.primecoder

import akka.actor.ActorRef
import akka.actor.ActorSystem
import akka.actor.Actor
import akka.event.Logging

import scala.collection.mutable.HashMap

class ScheduledActor extends Actor with akka.actor.ActorLogging {
  
  def receive: Actor.Receive = {
    case AddKeySignal =>
      val key = MutableSingleton.size+1
      val value = scala.util.Random.nextLong.toString
      log.info(s"Singleton receiving update signal : $key")
      log.info(s"... Updating $key -> $value")
      MutableSingleton.add(key, value)

    case GetKeySignal(key) =>
      log.info(s"Singleton receiving get signal : $key")
      log.info(s"... Obtaining $key -> ${MutableSingleton.get(key)}")
  }

}

object MutableSingleton {
  private var data = new HashMap[Int, String]

  def add(key: Int, value: String) = {
    data.addOne(key, value)
  }

  def get(key: Int) = {
    data.get(key)
  }

  def replace(m: HashMap[Int, String]) = {
    data = m
  }

  def size = data.size
}


