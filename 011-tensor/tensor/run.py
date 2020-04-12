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
  parser.add_argument('--ratio', dest='ratio', default=0.9, type=float,
    help='Ratio of training, ranging between 0-1')
  parser.add_argument("--batch", dest="batch", default=64, type=int,
    help="Size of each batch")
  parser.add_argument("--epoch", dest="epoch", default=3, type=int,
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

  # Reshape inputs (x,y)
  w = test_x[0].shape[0]
  train_x = np.array(train_x)
  train_x = train_x.reshape(len(train_y), w, w, 1)

  train_y = np.array(train_y).astype(float)
  
  # Feed to the model
  logging.info("Fitting the model")
  logging.debug("... Input shape : {}".format(train_x.shape))
  w = train_x[0].shape[0]
  m = build(w)
  m.fit(train_x, train_y, batch_size=cmdline.batch, epochs=cmdline.epoch)
  logging.debug("Fitting DONE")

  # Saving the model
  model_path = "model.bin"
  logging.info("Saving the model to {}".format(model_path))
  joblib.dump(m, model_path)
  logging.debug("Model SAVED")

  # Run test
  logging.info("Evaluating model")
  test_x = np.array(test_x)
  test_x = test_x.reshape(len(test_y), w, w, 1)
  test_y = np.array(test_y).astype(float)
  loss = m.evaluate(test_x, test_y, batch_size=cmdline.batch)
  logging.debug("... loss = {}".format(loss))


