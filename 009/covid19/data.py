import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from os import listdir
from os.path import isfile, join

def load_daily_cases(d):
  """
  Load all daily cases (CSV per date) from the containing directory
  @param d path to the directory containing daily case CSV files
  """

  # List all daily case files
  daily = [f for f in listdir(d) if isfile(join(d, f)) and f.endswith(".csv")]
  print(daily)