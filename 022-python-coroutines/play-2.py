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
    return chr(random.randint(65, 90)) # A-Z
  except asyncio.CancelledError:
    # Terminated
    print("... aborted GEN_CHAR")

async def gen_code():
  print("STARTING ...")
  task_gen_noise = asyncio.create_task(gen_noise())
  task_gen_char  = asyncio.create_task(gen_char())
  print("All tasks created.")

  await task_gen_char
  await task_gen_noise

  c = task_gen_char.result()
  n = task_gen_noise.result()

  print(c + str(n))
  return c + str(n)


random.seed(1)
loop = asyncio.get_event_loop()
tasks = [gen_code() for i in range(100)]

# Wait for 2 timeouts
wait_time = 0.1
wait_time2 = 0.4

finished, unfinished = loop.run_until_complete(
  asyncio.wait(tasks, timeout=wait_time)) # Wait 1st wave

finished2, unfinished = loop.run_until_complete(
  asyncio.wait(unfinished, timeout=wait_time2)) # Wait 2nd wave

n_finished = len(finished)
n_finished2 = len(finished2)
n_unfinished = len(unfinished)
print("----------------------------")
print(f"{n_finished} tasks finished within {wait_time} seconds")
print(f"{n_finished2} tasks finished within {wait_time2} seconds")
print(f"{n_unfinished} tasks unfinished")

all_finished = finished.union(finished2)
outcomes = [a.result() for a in all_finished]
print(f"all outcomes : {outcomes}")





