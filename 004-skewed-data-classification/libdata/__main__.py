"""
Main entry point 
for model training and classification
"""

import os
import pickle
import pandas as pd

from libdata import wrangle, func, feature, pipeline

def classification():
  pass

def training():
  pass

if __name__ == '__main__':
  print('Executing libdata ...')
  if os.path.isfile('model.pkl'):
    print('Model already exists, doing classification')
    classification()
  else:
    print('Start training process')
    training()