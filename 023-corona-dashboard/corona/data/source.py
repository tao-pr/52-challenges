import pandas as pd
import numpy as np

def read_covid19_data():
  url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
  print(f'Reading COVID-19 data from : {url}')
  return pd.read_csv(url)
