def add_feature_prev_temp(df):
  df.loc[df['month']==1, 'prev_month'] = 12
  df.loc[df['month']>1,  'prev_month'] = df['month'].apply(lambda n: n-1)
  df['prev_year'] = df['year'].apply(lambda n: n-1)
  
  df = df.merge(df[['AverageTemperature','month','year','Latitude','Longitude']], 
               left_on=['prev_month','prev_year','Latitude','Longitude'], 
               right_on=['month','year','Latitude','Longitude'],
               how='inner',
               suffixes=['','_prev'])
  
  df['temp_change'] = df['AverageTemperature'] - df['AverageTemperature_prev']
  df['temp'] = df['AverageTemperature']
  df['temp_prev'] = df['AverageTemperature_prev']

  df.drop(['month_prev','year_prev', 
          'AverageTemperature', 'AverageTemperature_prev'], axis=1, inplace=True)
  return df

def add_feature_latlng(df):
  trim = lambda r: r[:-1]
  df['lat'] = df['Latitude'].apply(trim)
  df['lng'] = df['Longitude'].apply(trim)
  return df
