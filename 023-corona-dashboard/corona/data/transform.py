import pandas as pd
import numpy as np

def aggregate_over_time(df, period='d'):
  if period='d':
    return df.groupby('date')
  elif period='w':
    # Counting week as 7 days from day zero, not by calendar year
    dates = df.date.unique()
    df_dates = pd.DataFrame({n: np.arange(len(dates)), date: dates})
    df_dates.loc[:, 'wk'] = df_dates['n'] // 7
    df = df.merge(df_dates[['date','wk']], on=['date'])
    return df.groupby('wk')
  elif period='m':
    strip_date_off = np.vectorize(lambda d: d[:7])
    df.loc[:, 'period'] = df['date'].apply(strip_date_off)
    return df.groupby('period')
  else:
    raise ValueError(f'Unsupported period : {period}')