"""
Needs Python 3.9
"""

import asyncio
import random
import time
import uuid
import os

def run_blocking_thread():
  # Create a file
  temp_file = str(uuid.uuid4()) + '.temp'
  with open(temp_file, 'w') as f:
    f.write('aaaaaa')

  # Wait (blocking) up to 2 sec
  time.sleep(random.randint(0,100))/50
  
  # Delete the file just created
  os.remove(temp_file)


async def run_concurrent_threads(num_threads):
  threads = [asyncio.to_thread(run_blocking_thread) for _ in range(num_threads)]
  await asyncio.gather(*threads)
  print(f"All {num_threads} threads finished")


# Start the loop
print('Starting ...')
asyncio.run(run_concurrent_threads(num_threads=5))
print('Ending ...')

