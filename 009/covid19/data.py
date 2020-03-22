import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from termcolor import colored
from os import listdir
from os.path import isfile, join

def load_daily_cases(d):
  """
  Load all daily cases (CSV per date) from the containing directory
  @param d path to the directory containing daily case CSV files
  """

  # List all daily case files
  q = join(d, "csse_covid_19_data/csse_covid_19_daily_reports")
  csv_list = [f for f in listdir(q) if isfile(join(q, f)) and f.endswith(".csv")]
  daily = []
  for tag in csv_list:
    print(colored("Reading : ", "cyan"), tag)
    with open(join(q,tag), "r") as f:
      # CSV is poorly formatted, there are preceding commas at the beginning
      # of many lines so let's read them manually
      header = []
      for l in f.readlines():
        tokens = l.split(",")

        # Register header if hasn't
        if len(header)==0:
          header = [a.replace("\n","") for a in tokens]
          continue

        # Empty preceding tokens (null province)
        # will be replaced with country name (subsequent token)
        if len(tokens[0])==0:
          tokens[0] = tokens[1]

        kv = {a: b for a,b in zip(header,tokens)}

        # Also add "date" as another column
        kv["date"] = tag.split(".")[0] 
        daily.append(kv)

  daily = pd.DataFrame(daily)
  print(daily[:5])
  print(daily.columns)
  print(colored("Daily records read : ", "cyan"), len(daily), " rows")
  return daily


if __name__ == '__main__':
  """
  Usage: 
    python3 -m covid19.data {PATH_TO_COVID19_GIT_REPOPATH}
  """
  path = sys.argv[-1]
  print(colored("Loading daily cases from : ","cyan"), path)
  daily = load_daily_cases(path)