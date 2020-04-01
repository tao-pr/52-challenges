import sys
import joblib
import pickle
import numpy as np

from .data import Deep

if __name__ == '__main__':
  arg1 = sys.argv[-2]
  arg2 = sys.argv[-1]

  if arg1 not in ["PICKLE","JOBLIB","JOBLIB-COMPRESS"]:
    raise ValueError("Unknown run mode")

  if arg1 == "PICKLE":
    if arg2 == "WRITE":
      blob = Deep()
      print("Serialising with pickle")
      with open("pickle", "wb") as f:
        pickle.dump(blob, f)
    else:
      print("Deserialising with pickle")
      with open("pickle", "rb") as f:
        blob = pickle.load(f)

  elif arg1 == "JOBLIB":
    if arg2 == "WRITE":
      print("Serialising with joblib")
      blob = Deep()
      with open("joblib", "wb") as f:
        joblib.dump(blob, f)
    else:
      print("Deserialising with joblib")
      with open("joblib", "rb") as f:
        blob = joblib.load(f)

  elif arg1 == "JOBLIB-COMPRESS":
    if arg2 == "WRITE":
      print("Serialising with joblib compression")
      blob = Deep()
      with open("joblib-compressed", "wb") as f:
        joblib.dump(blob, f, compress=1)
    else:
      print("Deserialising with joblib compression")
      with open("joblib-compressed", "rb") as f:
        blob = joblib.load(f)

