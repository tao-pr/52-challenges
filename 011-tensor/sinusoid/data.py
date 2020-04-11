import pandas as pd
import numpy as np

from typing import Tuple

def gen_sinusoid(length: int, mag: double, range_: Tuple[double,double]):
  """
  Generate a sequence of sinusoid
  """
  a,b = range_
  step = (b-a)/length
  return mag * np.sin(np.arange(a, b, step))

def gen_dataset(num: int, length: int):
  """
  Generate a dataset containing sinusoid data
  """
  dset = []
  for i in range(num):
    m = abs(np.random.normal(10, 1.5))
    a = np.random.uniform()
    rg = (np.pi * -a, np.pi * a)
    dset.append((m,a,gen_sinusoid(length, m, rg)))
  return dset


