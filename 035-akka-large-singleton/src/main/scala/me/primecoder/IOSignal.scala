package me.primecoder

import akka.actor.typed.ActorRef
import akka.actor.typed.ActorSystem
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors
import akka.actor.Props
import scala.concurrent.duration._

private [primecoder] trait IOSignal

final case object AddKeySignal extends IOSignal
final case class UpdateKeySignal(key: Int, value: String) extends IOSignal
final case object BulkReplaceSignal extends IOSignal
final case class GetKeySignal(key: Int) extends IOSignal