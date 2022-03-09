package me.primecoder

import akka.actor.ActorRef
import akka.actor.ActorSystem
import akka.actor.Actor
import akka.event.Logging

import scala.collection.mutable.HashMap

class ScheduledActor extends Actor with akka.actor.ActorLogging {
  
  def receive: Actor.Receive = {
    case AddKeySignal =>
      // Add 20000 keys at a time
      log.info(s"Scheduler receiving update signal - updating ${ScheduledActor.CONCURRENT_UPDATE_SIZE} keys")
      for (i <- 1 to ScheduledActor.CONCURRENT_UPDATE_SIZE){
        if (MutableSingleton.size < ScheduledActor.MAX_KEYS){
          val key = MutableSingleton.size+1  
          val value = scala.util.Random.nextLong.toString
          MutableSingleton.add(key, value)
        } 
      }
      log.info(s"... Singleton now has ${MutableSingleton.size} keys")

    case BulkReplaceSignal =>
      // Large update and replace
      log.info(s"Scheduler receiving bulk update signal - ${MutableSingleton.size} keys")
      val m = HashMap[Int,String](MutableSingleton.getKeys.map{ k => (k, "old")}.toSeq :_*)
      MutableSingleton.replace(m)

    case GetKeySignal(key) =>
      log.info(s"Scheduler receiving get signal : $key")
      log.info(s"... Obtaining $key -> ${MutableSingleton.get(key)}")
  }

}

object ScheduledActor {
  val MAX_KEYS = 1.3e6
  val CONCURRENT_UPDATE_SIZE = 50000
}

object MutableSingleton {
  private var data = new HashMap[Int, String]

  def add(key: Int, value: String) = {
    data.addOne(key, value)
  }

  def getKeys = data.keys

  def get(key: Int) = {
    data.get(key)
  }

  def replace(m: HashMap[Int, String]) = {
    data = m
  }

  def size = data.size
}


