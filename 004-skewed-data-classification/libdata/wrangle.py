import pandas as pd
import numpy as np
from typing import List

from libdata.func import collect, head

def split_month_year(df: pd.DataFrame) -> pd.DataFrame:
  """
  Split the `dt` column into `year` and `month`
  """
  df['dt'] = pd.to_datetime(df['dt'])
  df['year'] = df['dt'].dt.to_period('Y').apply(lambda period: period.year)
  df['month'] = df['dt'].map(lambda d: d.month)
  df.reset_index(inplace=True, drop=True)
  return df

def take_last_year(city_df: pd.DataFrame, num_years: int = 1) -> pd.DataFrame:
  """
  Filter the last year only
  """
  df = city_df[city_df['year'] >= max(city_df['year']) - num_years + 1]
  df = df[[
    'AverageTemperature','month','City','Country',
    'Latitude','Longitude']]
  return df

def agg_monthly_climate(city_df: pd.DataFrame) -> pd.DataFrame:
  """
  Collect monthly climate over coordinates
  """
  agg = city_df.groupby(['Latitude','Longitude']).agg({
    'AverageTemperature': [min, max, collect]
  }).reset_index(drop=False)
  return agg

def create_city_latlng_map(city_df: pd.DataFrame) -> dict:
  """
  Create a dictionary which maps from lat-lng coordinate to the city name
  """
  agg = city_df.groupby(['Latitude','Longitude']).agg({
    'City': head, 'Country': head
  }).reset_index(drop=False)
  
  m = dict()
  for _,row in agg.iterrows():
    key = '{}-{}'.format(row['Latitude'], row['Longitude'])
    m[key] = (row['City'], row['Country'])
  return m