import sys
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

from termcolor import colored

from covid19.data import *

def plot_daily_cases(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    plt.plot(cnt["Confirmed"], label=c)

  plt.xlabel("Day")
  plt.ylabel("Cases")
  plt.title("Accumulated Cases Daily, since 100th case")
  plt.legend()
  fig.show()

def plot_daily_patients(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    plt.plot(cnt["Patients"], label=c)

  plt.figure(figno)
  plt.xlabel("Day")
  plt.ylabel("Cases")
  plt.title("Accumulated Active Patients Daily, since 100th case")
  plt.legend()
  fig.show()


def plot_daily_increment(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case

    # Movine average for smoothening
    cnt["sma"] = 100 * cnt["new_confirmed"].rolling(window=5).mean()
    plt.plot(cnt["sma"], label=c)

  plt.xlabel("Day")
  plt.ylabel("% Increase")
  plt.title("Case Incremental Rate %, since 100th case")
  plt.legend()
  fig.show()

def plot_recovery_rate(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    cnt["ratio_recovered"] = 100 * cnt["ratio_recovered"]
    plt.plot(cnt["ratio_recovered"], label=c)

  # Plot recovery pivot point (7 days)
  plt.axvline(x=7, ymin=0, ymax=100, linestyle="dotted")

  plt.xlabel("Day")
  plt.ylabel("% Recovered")
  plt.title("Percentage of recovery, since 100th case")
  plt.legend()
  fig.show()


def plot_mortal_rate(figno, step, countries):
  """
  Starting from 100th case of the nation
  """
  fig = plt.figure(figno)
  for c in countries:
    cnt = step[(step["Country/Region"]==c) & (step["Confirmed"]>=100)]
    cnt.index = np.arange(0, len(cnt)) # Index by num of days from 100th case
    cnt["ratio_death"] = 100 * cnt["ratio_death"]
    plt.plot(cnt["ratio_death"], label=c)

  # Plot recovery pivot point (7 days)
  plt.axvline(x=7, ymin=0, ymax=100, linestyle="dotted")

  plt.xlabel("Day")
  plt.ylabel("% Mortal")
  plt.title("Mortal rate, since 100th case")
  plt.legend()
  fig.show()


if __name__ == '__main__':
  """
  Usage:
  
    python3 -m covid19.plot {PATH_TO_COVID19_GIT_REPOPATH}

  """
  path = sys.argv[-1]
  print(colored("Loading daily cases from : ","cyan"), path)
  
  # Load and wrangle daily report data
  daily   = load_daily_cases(path)
  wranged = wrang_data(daily)
  step    = make_daily_step(wranged)

  step = step.reset_index(drop=False)

  countries = ["Thailand","Germany","Italy","France","US","UK","South Korea","Japan","Iran"]

  # Plot
  plot_daily_cases(1, step, countries)
  plot_daily_patients(2, step, countries)
  plot_daily_increment(3, step, countries)
  plot_recovery_rate(4, step, countries)
  plot_mortal_rate(5, step, countries)
  input("Press RETURN to end ...")