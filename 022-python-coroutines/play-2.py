"""
More complex coroutines
with native Python 3.7's async
"""

import asyncio
import random
import time

async def gen_noise():
  # Delay by random (0-1 sec)
  await asyncio.sleep(random.randint(0,10)/10)
  return random.randint(0,100)

async def gen_char():
  # Delay by random (0-1 sec)
  try:
    await asyncio.sleep(random.randint(0,10)/10)
    return char(random.randint(65, 90)) # A-Z
  except asyncio.CancelledError:
    # Terminated
    print("... aborted GEN_CHAR")

async def gen_code():
  print("STARTING ...")
  task_gen_noise = asyncio.create_task(gen_noise())
  task_gen_char  = asyncio.create_task(gen_char())
  print("All tasks created.")

  c = await task_gen_char()
  n = await task_gen_noise()
  print(c + str(n))
  return c + str(n)


random.seed(1)
loop = asyncio.get_event_loop()
tasks = [gen_code() for i in range(100)]

finished, unfinished = loop.run_until_complete(
  asyncio.wait(tasks, timeout=0.3))

n_finished = len(finished)
n_unfinished = len(unfinished)
print("----------------------------")
print(f"{n_finished} tasks finished")
print(f"{n_unfinished} tasks unfinished")


