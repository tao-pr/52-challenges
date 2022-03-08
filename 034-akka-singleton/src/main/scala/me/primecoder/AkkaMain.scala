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

  // Start scheduler
  val tick = actorSystem.actorOf(Props(classOf[ScheduledActor]))
  val scheduler: Cancellable = actorSystem.scheduler.scheduleWithFixedDelay(
    5.seconds, // delay of first run
    10.seconds, // frequency
    tick,
    AddKeySignal
  )

  sys.addShutdownHook{
    scheduler.cancel
    actorSystem.terminate
  }
}

