import pandas as pd
import numpy as np

def split_month_year(df):
  df['dt'] = pd.to_datetime(df['dt'])
  df['year'] = df['dt'].dt.to_period('Y').apply(lambda period: period.year)
  df['month'] = df['dt'].map(lambda d: d.month)
  df.reset_index(inplace=True, drop=True)
  return df

def take_last_year(city_df):
  df = city_df[city_df['year']==max(city_df['year'])]
  df = df[[
    'AverageTemperature','month','City','Country',
    'Latitude','Longitude']]
  return df

def agg_to_grid(city_df):
  pass