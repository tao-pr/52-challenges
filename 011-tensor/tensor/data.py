import pandas as pd
import numpy as np
import logging
import joblib
import cv2
import argparse
import sys
import os

from typing import Tuple
from termcolor import colored


# Log to file and print to stdout simulteneously
logging.basicConfig(filename='tensor.log',level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s')
logging.getLogger().addHandler(logging.StreamHandler())


def gen_images(n: int, dim: Tuple[int,int], noise_level: float, f): 
  """
  Generate an image dataset
  Args:
    n (int):              Size of the dataset
    dim (int,int):        Dimension of the image, height x weight
    noise_level (double): Ratio of noise (0-1)
    f (function):         Function to apply with generated image
  """
  h,w = dim
  num_noise_pixels = int(noise_level * w * h)

  def add_noise(im):
    for i in range(num_noise_pixels):
      x = int(np.random.choice(range(w)))
      y = int(np.random.choice(range(h)))
      im[y,x] = 255
    return im

  dset = []
  for i in range(n):
    # Generate background
    im = np.ones((h,w,1), np.uint8) * int(np.random.choice([
      25, 50, 100, 128, 150, 200, 250
      ]))
    # Generate crosshair
    x = np.random.choice(range(w))
    y = np.random.choice(range(h))
    cv2.line(im, (0,y), (w,y), (0,0,0), 1)
    cv2.line(im, (x,h), (x,0), (0,0,0), 1)
    im = add_noise(im)
    hashstr = joblib.hash(im)
    dset.append((hashstr,im, x, y))
    if f is not None:
      f(hashstr, im)
  return dset

def gen_dataset(n: int, dim: Tuple[int,int], f):
  """
  Generate the whole dataset consisting 10 portions
  1. Without noise
  2. With 5% noise
  3. With 15% noise
  4. With 50% noise
  5. With random noise between 15~50%
  """
  noises = [0, 0.05, 0.15, 0.5, np.random.choice(np.arange(0.15,0.5,0.1))]

  rows = []
  psize = n//5
  remain = n-(n//5)*5
  for i,n in enumerate(noises):
    m = "Generating images in portion #{}/5, noise level = {:.2f}".format(
      i+1, n)
    logging.info(m)
    
    # The last portion will include the remainder
    if i==len(noises)-1:
      psize += remain

    images = gen_images(int(psize), dim, n, f)
    for hashstr,im, x, y in images:
      filename = "{}.jpg".format(hashstr)
      rows.append((filename, n, x, y))
  print("Generating dataframe")
  logging.info("Generating dataframe of size {}".format(len(rows)))
  df = pd.DataFrame(rows, columns=["filename","noise","x","y"])
  return df

def save_image(path):
  def to(hashstr, im):
    p = "{}.jpg".format(os.path.join(path, hashstr))
    m = "... Saving image to {}".format(p)
    logging.debug(m)
    cv2.imwrite(p, im)
  return to

def create_dir(path):
  if not os.path.exists(path) and not os.path.isfile(path):
    logger.info("Creating directory : {}".format(path))
    os.mkdir(path)

def commandline():
  """
  Create an instance of argument parser
  """
  parser = argparse.ArgumentParser(description='Dataset generator')
  parser.add_argument('--saveto', dest='saveto', default='data',
    help='Path to store the output')
  parser.add_argument('--size', dest='size', default=100, type=float,
    help='Size of the dataset to generate')
  parser.add_argument('--dim', dest='dim', default=256, type=int,
    help='Dimension of the image to generate (square)')

  args = parser.parse_args()
  return args

class DataSet(object):
  """
  Dataset handler
  """
  def __init__(self, path: str):
    self.path = path

  def load_split(self, ratio: float):
    """
    Load the whole images and split into train and test
    """
    csvpath = os.path.join(self.path, "dataset.csv")
    df = pd.read_csv(csvpath, sep=',')

    getx = lambda row: cv2.imread(os.path.join(self.path, row["filename"]), cv2.IMREAD_GRAYSCALE)
    gety = lambda row: row[["x","y"]]

    logging.info("Loading image dataset of size : {}".format(len(df)))
    dd = [(getx(row),gety(row)) for i,row in df.iterrows()]

    logging.info("Splitting image dataset into {:.0f} % for testing".format((1-ratio)*100))
    indices = np.arange(len(df))
    np.random.shuffle(indices)
    ta, tb = [],[]
    for i,row in zip(indices,dd):
      if i<int(ratio * len(df)):
        ta.append(row)
      else:
        tb.append(row)

    logging.debug("Split DONE")
    logging.debug("... Training size : {}".format(len(ta)))
    logging.debug("... Test size     : {}".format(len(tb)))

    return [ta,tb]


if __name__ == '__main__':
  """
  Generate a dataset onto the specified path
  """
  cmdline = commandline()
  create_dir(cmdline.saveto)

  print(colored("Starting dataset generator", "cyan"))

  # Generate images to the specified directory
  # with csv file named "dataset.csv" inside
  dset = gen_dataset(
    cmdline.size,
    (cmdline.dim, cmdline.dim),
    save_image(cmdline.saveto))
  
  path_csv = os.path.join(cmdline.saveto, "dataset.csv")
  print("Saving dataframe to {}".format(path_csv))
  dset.to_csv(path_csv, sep=',', header=True, index=False)

