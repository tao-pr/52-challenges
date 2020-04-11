import pandas as pd
import numpy as np
import cv2
import argparse
import sys
import os

from typing import Tuple

def gen_dataset(n: int, dim: Tuple[int,int], noise_level: float): 
  """
  Generate an image dataset
  Args:
    n (int):              Size of the dataset
    dim (int,int):        Dimension of the image, height x weight
    noise_level (double): Ratio of noise (0-1)
  """
  h,w = dim
  num_noise_pixels = int(noise_level * w * h)

  def add_noise(im):
    for i in num_noise_pixels:
      x = int(np.random.choice(range(w)))
      y = int(np.random.choice(range(h)))
      im[y,x] = 255
    return im

  dset = []
  for i in range(n):
    # Generate background
    im = np.ones(dim, cv2.uint8) * int(np.random.choice([
      25, 50, 100, 128, 150, 200, 250
      ]))
    # Generate crosshair
    x = np.random.choice(range(w))
    y = np.random.choice(range(h))
    cv2.line(im, (0,y), (w,y), (0,0,0), 1)
    cv2.line(im, (x,h), (x,0), (0,0,0), 1)
    im = add_noise(im)
    dset.append(im)
  return dset


def commandline():
  """
  Create an instance of argument parser
  """
  parser = argparse.ArgumentParser(description='Dataset generator')
  parser.add_argument('--saveto', dest='path', default='data',
    help='Path to store the output')
  parser.add_argument('--size', dest='size', default=100,
    help='Size of the dataset to generate')
  parser.add_argument('--dim', dest='dim', default=256,
    help='Dimension of the image to generate (square)')

  args = parser.parse_args()
  return args

if __name__ == '__main__':
  """
  Generate a dataset onto the specified path
  """
  cmdline = commandline()




