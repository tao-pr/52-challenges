import tensorflow as tf
import numpy as np
import joblib

import argparse
import sys
import os

from .model import build

def commandline():
  """
  Create an instance of argument parser
  """
  parser = argparse.ArgumentParser(description='Model runner')
  parser.add_argument('--datapath', dest='path', default='data',
    help='Path to read data from')
  args = parser.parse_args()
  return args

# TAOTODO Main entry
if __name__ == '__main__':
  cmdline = commandline()
  pass