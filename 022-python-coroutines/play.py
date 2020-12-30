import asyncio

def worker():
  print('Reading ...')
  while True:
    v = (yield)
    if v=='stop':
      print('[BREAKING]')
      break
    else:
      print(f'Receiving ... {v}')

# Start a coroutine
w = worker()
w.__next__()

# Send value to (yield)
w.send("a")
w.send("b")
w.send("c")
w.send("stop")
