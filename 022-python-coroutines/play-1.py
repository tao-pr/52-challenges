"""
Single coroutine
"""

def worker():
  print('Reading ...')
  try:
    while True:
      v = (yield)
      if v=='stop':
        print('[BREAKING]')
        break
      else:
        print(f'Receiving ... {v}')
  except GeneratorExit: # Termination signal
    print('[Terminating coroutine]')


# Start a coroutine
w = worker()
next(w)

w.send("a")
w.send("b")
w.send("c")
w.send("d")
w.close()
