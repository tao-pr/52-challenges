"""
Main entry point 
for model training and classification
"""

import os
import pickle
import pandas as pd

from libdata import wrangle, func, feature, pipeline

def load_csv(filename):
  city_temp_file = os.path.join(
    os.environ['HOME'], 
    'data',
    'global-temperature',
    filename)
  print('Reading {}'.format(city_temp_file))
  return pd.read_csv(city_temp_file)

def get_clean_data(for_train: bool):
  """
  Load raw data from a csv file.
  Polish features and discard unwanted columns.
  """

  if for_train and os.path.isfile('features_train.csv'):
    print('Loading the precooked feature file')
    df = pd.read_csv('features_train.csv')
    print('Feature size : {}'.format(len(df)))
    return df
  else:
    df = load_csv('GlobalLandTemperaturesByCity.csv')
    print('Polishing features')
    df = wrangle.split_month_year(df)
    df = df[['AverageTemperature','City','Country',
             'Latitude','Longitude',
             'year','month']]
    df = df[df['AverageTemperature'].notnull()]

    print('Filtering data')
    if for_train:
      df = df[(df['year']>=1900) & (df['year']<=2000)].sample(frac=0.02)
    else:
      df = df[(df['year']>=2001) & (df['year']<=2010)]

    print('Raw data size for feature polish : {}'.format(len(df)))
    features = feature.add_feature_prev_temp(df)
    features = feature.add_feature_latlng(features)
    features.drop(['City','Latitude','Longitude'], axis=1, inplace=True)
    print('Feature size : {}'.format(len(features)))
    print('Saving feature file')
    features.to_csv('features_train.csv', sep=',')
    return features

def classification():
  df = get_clean_data(for_train=False)
  model = pickle.load(open('model.pkl', 'rb'))
  print('Ready for classification ...')
  pass

def training():
  df = get_clean_data(for_train=True)
  print('Ready for training ...')
  print('Training data size : {}'.format(len(df)))
  print('Training ...')
  df_fitted = pipeline.clf.fit_transform(df)

if __name__ == '__main__':
  print('Executing libdata ...')
  if os.path.isfile('model.pkl'):
    print('Running classification with pre-trained model')
    classification()
  else:
    print('Starting training process')
    training()