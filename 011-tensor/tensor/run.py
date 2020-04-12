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
  parser.add_argument("--batch", dest="batch", default=64,
    help="Size of each batch")
  parser.add_argument("--epoch", dest="epoch", default=3,
    help="Number of epochs to run")
  args = parser.parse_args()
  return args


if __name__ == '__main__':
  cmdline = commandline()

  logging.info("Tensor run started")
  logging.info("... Data path : {}".format(cmdline.path))
  logging.info("... Ratio of training : {:.2f}".format(cmdline.ratio))

  if not os.path.exists(cmdline.path) or os.path.isfile(cmdline.path):
    raise FileNotFoundError("Unable to find data path : {}".format(cmdline.path))

  # Load and split the dataset
  ds = DataSet(cmdline.path)
  train,test = ds.load_split(cmdline.ratio)
  train_x, train_y = zip(*train)
  test_x, test_y   = zip(*test)
  
  # Feed to the model
  logging.info("Fitting the model")
  m = build()
  m.fit(train_x, test_x, batch_size=cmdline.batch, epochs=cmdline.epoch)
  logging.debug("Fitting DONE")

  # Saving the model
  model_path = "model.bin"
  logging.info("Saving the model to {}".format(model_path))
  joblib.dump(m, model_path)
  logging.debug("Model SAVED")

  # Run test
  logging.info("Evaluating model")
  loss = m.evaluate(test_x, test_y, batch_size=cmdline.batch)
  logging.debug("... loss = {}".format(loss))

