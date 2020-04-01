import sys
import pickle
import joblib
import numpy as np

from .data import Deep

if __name__ == '__main__':
  arg1 = sys.argv[-2]
  arg2 = sys.argv[-1]

  if arg1 not in ["PICKLE","JOBLIB"]:
    raise ValueError("Unknown run mode")

  if arg1 == "PICKLE":
    if arg2 == "WRITE":
      blob = Deep()
      print("Serialising with pickle")
      with open("pickle", "w") as f:
        pickle.dump(blob, f)
    else:
      print("Deserialising with pickle")
      with open("pickle", "r") as f:
        blob = pickle.load(f)

  elif arg1 == "JOBLIB":
    if arg2 == "WRITE":
      print("Serialising with joblib")
      blob = Deep()
      print("Serialising with joblib")
      with open("joblib", "w") as f:
        joblib.dump(blob, f)
    else:
      print("Deserialising with joblib")
      with open("joblib", "r") as f:
        blob = joblib.load(f)

