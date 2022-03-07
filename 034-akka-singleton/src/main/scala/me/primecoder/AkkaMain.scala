//#full-example
package me.primecoder


import akka.actor.typed.ActorRef
import akka.actor.typed.ActorSystem
import akka.actor.typed.Behavior
import akka.actor.typed.scaladsl.Behaviors

object MainActor {
  private [primecoder] trait IOSignal
  final case object StartUpSignal extends IOSignal
  final case object ShutdownSignal extends IOSignal
  final case class UpdateSignal(key: String, value: Int) extends IOSignal
  final case class GetSignal(key: String) extends IOSignal

  def apply(): Behavior[IOSignal] = 
    Behaviors.setup { context =>
        Behaviors.receiveMessage { signal => 
          // TODO:
          context.log.info(s"MainActor receiving signal : ${signal}")
          Behaviors.same
        }
    }
}

// -object GreeterBot {
// -
// -  def apply(max: Int): Behavior[Greeter.Greeted] = {
// -    bot(0, max)
// -  }
// -
// -  private def bot(greetingCounter: Int, max: Int): Behavior[Greeter.Greeted] =
// -    Behaviors.receive { (context, message) =>
// -      val n = greetingCounter + 1
// -      context.log.info("Greeting {} for {}", n, message.whom)
// -      if (n == max) {
// -        Behaviors.stopped
// -      } else {
// -        message.from ! Greeter.Greet(message.whom, context.self)
// -        bot(n, max)
// -      }


// object GreeterMain {

//   final case class SayHello(name: String)

//   def apply(): Behavior[SayHello] =
//     Behaviors.setup { context =>
//       //#create-actors
//       val greeter = context.spawn(Greeter(), "greeter")
//       //#create-actors

//       Behaviors.receiveMessage { message =>
//         //#create-actors
//         val replyTo = context.spawn(GreeterBot(max = 3), message.name)
//         //#create-actors
//         greeter ! Greeter.Greet(message.name, replyTo)
//         Behaviors.same
//       }
//     }
// }

//#main-class
object MainRun extends App {
  implicit val actorSystem: ActorSystem[MainActor.IOSignal] = ActorSystem(MainActor(), "MainRun")

  Console.println("Starting app ...")
}

