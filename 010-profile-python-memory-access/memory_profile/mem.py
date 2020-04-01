import sys
import numpy as np
from memory_profiler import profile

from .data import M

def inplace_ref_write(ms):
  [m.update() for m in ms]


def gen_new_array_inplace_ref_write(ms):
  return [m.update() for m in ms]


if __name__ == '__main__':
  arg = sys.argv[-1]

  if arg not in ["INPLACE","NEW_ARRAY_SAME_REF","REF_NEW"]:
    raise ValueError("Unknown mode to run")

  n_loop = 5

  # Create large object
  p = []
  obj = [M() for i in range(1000)]

  for n in range(n_loop):
    print("iter #", n)

    if arg=="INPLACE":
      # In-place update the memory without copying, return nothing
      inplace_ref_write(obj)

    elif arg=="NEW_ARRAY_SAME_REF":
      # Return a reference to the updated memory, replace the existing one
      obj = gen_new_array_inplace_ref_write(obj)
