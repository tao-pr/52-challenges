import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def aggregate_over_time(df, period='d', aggregator={'total_cases': 'sum'}):
  if period='d':
    dfg = df.groupby('date')
  elif period='w':
    # Counting week as 7 days from day zero, not by calendar year
    dates = df.date.unique()
    df_dates = pd.DataFrame({n: np.arange(len(dates)), date: dates})
    df_dates.loc[:, 'wk'] = df_dates['n'] // 7
    dfg = df.merge(df_dates[['date','wk']], on=['date']).groupby('wk')
  elif period='m':
    strip_date_off = np.vectorize(lambda d: d[:7])
    df.loc[:, 'period'] = df['date'].apply(strip_date_off)
    dfg = df.groupby('period')
  else:
    raise ValueError(f'Unsupported period : {period}')

  dfg = dfg.agg(aggregator)
  return dfg.reset_index()

def plot_agg(df, country_list=['Germany'], aggregator={'total_cases': 'sum'}, period='d'):
  dfg = aggregate_over_time(
    df=df[df.location.isin(country_list)],
    period=period,
    aggregator=aggregator)
  
  # TAOTODO plot it