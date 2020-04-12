import tensorflow as tf
import numpy as np
import joblib
import logging
import json

import argparse
import sys
import os
import cv2

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
  parser.add_argument("--outputpath", dest='out', default='out',
    help='Output path to store visual predictions')
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
  train,test                     = ds.load_split(cmdline.ratio)
  train_x, train_y, _            = zip(*train)
  test_x, test_y, test_filenames = zip(*test)

  # Reshape inputs (x,y), and make sure they are floating (tensor-compatible)
  h,w     = test_x[0].shape[0], test_x[0].shape[1]
  train_x = np.array(train_x)
  train_x = train_x.reshape(len(train_y), w, w, 1)
  train_y = np.array(train_y).astype(float)

  test_x = np.array(test_x)
  test_x = test_x.reshape(len(test_y), w, w, 1)
  test_y = np.array(test_y).astype(float)
  
  # Train & validate
  logging.info("Fitting the model")
  logging.debug("... Input shape : {}".format(train_x.shape))
  w = train_x[0].shape[0]
  m = build(w)
  h = m.fit(
    train_x, train_y, 
    batch_size=cmdline.batch, 
    epochs=cmdline.epoch,
    validation_data=(test_x, test_y))
  logging.debug("Fitting DONE")

  # Save fitting history as json
  with open("history-train.json", "w") as f:
    logging.info("Saving history of fitting epochs as json")
    json.dump(h, f, indent=2)

  # Save model (only weights)
  logging.info("Saving model to model.checkpoint")
  m.save_weights("model.checkpoint")
  logging.debug("... Model SAVED")

  # Render the predictions
  if not os.path.exists(cmdline.out) and not os.path.isfile(cmdline.out):
    os.mkdir(cmdline.out)

  logging.info("Evaluating model")
  loss = m.evaluate(test_x, test_y, batch_size=cmdline.batch)
  logging.info("... loss = {}".format(loss))

  logging.info("Rendering visual predictions")
  logging.info("... Test size : {}".format(len(test_x)))
  out = predict(test_x)
  for x,y,filename in zip(out, test_filenames):
    fullpath     = os.path.join(cmdline.out, filename)
    originalpath = os.path.join(cmdline.path, filename)
    logging.debug("... Saving output to {}".format(fullpath))
    
    im = cv2.read(originalpath)
    if y>=0 and y<h:
      cv2.line(im, (0,y), (w,y), (245,0,0), 1)
    if x>=0 and x<w:
      cv2.line(im, (x,0), (x,h), (245,0,0), 1)
    cv2.imwrite(fullpath, im)



