//#full-example
package me.primecoder


import akka.actor.ActorRef
import akka.actor.ActorSystem
import akka.actor.Props
import akka.actor.Cancellable
import akka.event.Logging

import com.typesafe.config.ConfigFactory
import scala.concurrent.ExecutionContextExecutor
import scala.concurrent.duration._

object MainRun extends App {
  lazy val appConfig = ConfigFactory.load()
  implicit lazy val actorSystem = ActorSystem("MainActor")
  implicit lazy val ec: ExecutionContextExecutor = actorSystem.dispatcher

  // Start schedulers
  val tickUpdate = actorSystem.actorOf(Props(classOf[ScheduledActor]))
  val schedulerUpdate: Cancellable = actorSystem.scheduler.scheduleWithFixedDelay(
    1.seconds, // delay of first run
    1.seconds, // frequency
    tickUpdate,
    AddKeySignal
  )

  val tickBulkUpdate = actorSystem.actorOf(Props(classOf[ScheduledActor]))
  val schedulerBulkUpdate: Cancellable = actorSystem.scheduler.scheduleWithFixedDelay(
    4.seconds, // delay of first run
    3.seconds, // frequency
    tickBulkUpdate,
    BulkReplaceSignal
  )

  // Delayed loop which keeps reading singleton object
  while (true){
    Thread.sleep(250)
    val keysize = MutableSingleton.size
    if (keysize > 0){
      val key = scala.util.Random.nextInt.abs % keysize
      val v = MutableSingleton.get(key).map(_.toString).getOrElse("N/A")
      Console.println(s"[Deferred] Randomly checking key $key -> $v (singleton map size : ${keysize})")
    }
  }

  sys.addShutdownHook{
    schedulerUpdate.cancel
    schedulerBulkUpdate.cancel
    actorSystem.terminate
  }
}

