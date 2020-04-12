import tensorflow as tf
import numpy as np
import joblib
import logging

import argparse
import sys
import os

from .model import build
from .data import DataSet

# Log to file and print to stdout simulteneously
logging.basicConfig(filename='tensor.log',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
logging.getLogger().addHandler(logging.StreamHandler())


def commandline():
  """
  Create an instance of argument parser
  """
  parser = argparse.ArgumentParser(description='Model runner')
  parser.add_argument('--datapath', dest='path', default='data',
    help='Path to read data from')
  parser.add_argument('--ratio', dest='ratio', default=0.9,
    help='Ratio of training, ranging between 0-1')
  args = parser.parse_args()
  return args

# TAOTODO Main entry
if __name__ == '__main__':
  cmdline = commandline()

  logging.info("Tensor run started")
  logging.info("... Data path : {}".format(cmdline.path))
  logging.info("... Ratio of training : {:.2f}".format(cmdline.ratio))

  if not os.path.exists(cmdline.path) or os.path.isfile(cmdline.path):
    raise FileNotFoundError("Unable to find data path : {}".format(cmdline.path))

  # Load CSV describing the whole dataset
  ds = DataSet(cmdline.path)
  train,test = ds.load_split(cmdline.ratio)
  pass