import pandas as pd
import numpy as np
import plotly.express as px
import traceback

def aggregate_over_time(df, period='d', aggregator={'total_cases': 'sum'}):
  if period=='d':
    print(f'... aggregate_over_time (daily) : aggregator = {aggregator}')
    dfg, tick_col = (df.groupby(['date', 'location']), 'date')
  elif period=='w':
    print(f'... aggregate_over_time (weekly) : aggregator = {aggregator}')
    # Counting week as 7 days from day zero, not by calendar year
    dates = df.date.unique()
    df_dates = pd.DataFrame({'n': np.arange(len(dates)), 'date': dates})
    df_dates.loc[:, 'wk'] = df_dates['n'] // 7
    dfg = df.merge(df_dates[['date','wk']], on=['date']).groupby(['wk', 'location'])
    tick_col = 'wk'
  elif period=='m':
    print(f'... aggregate_over_time (monthly) : aggregator = {aggregator}')
    strip_date_off = np.vectorize(lambda d: d[:7])
    df.loc[:, 'month'] = df['date'].apply(strip_date_off)
    dfg, tick_col = (df.groupby(['month', 'location']), 'month')
  else:
    raise ValueError(f'Unsupported period : {period}')

  print('... aggregating over period')
  dfg = dfg.agg(aggregator)
  return (dfg.reset_index(), tick_col)

def plot_agg(df, country_list=['Germany'], aggregator={'total_cases': 'sum'}, period='d'):
  dfg, tick_col = aggregate_over_time(
    df=df[df.location.isin(country_list)],
    period=period,
    aggregator=aggregator)
  try:
    fig = px.line(dfg, x=tick_col, y=list(aggregator.keys())[0], color="location")
  except:
    print(traceback.format_exc())
  return fig