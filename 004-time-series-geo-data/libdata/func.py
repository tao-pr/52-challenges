import pandas as pd
import numpy as np
from typing import List

def collect(s: pd.Series) -> List[float]:
  return list(s)

def head(s: pd.Series) -> str:
  return s.values[0] # TIPS: Technically faster than .iloc[0]

def avg(ns: List[float]) -> float:
  return np.mean(ns)

def avg_of_avg(ns: List[List[float]]) -> float:
  return np.mean([np.mean(n) for n in ns])

def min_of_min(ns: List[List[float]]) -> float:
  return np.min([np.min(n) for n in ns])

def max_of_max(ns: List[List[float]]) -> float:
  return np.max([np.max(n) for n in ns])