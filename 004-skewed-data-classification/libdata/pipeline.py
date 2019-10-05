from sklearn.pipeline import *
from sklearn.base import BaseEstimator, TransformerMixin

clf = make_pipeline(
  memory=None,
  steps=[
    ('FeatureSelector', ColumnsSelector()),
    ('CountryEncoder', CountryEncoder()),
    ])

class ColumnsSelector(BaseEstimator, TransformerMixin):
  
  def __init__(self):
    pass

  def fit(self, X, y=None):
    return self

  def transform(self, X, y=None): 
    return X[['Country','year','month','prev_month','temp_change','temp_prev',
              'lat','lng']]


class CountryEncoder(BaseEstimator, TransformerMixin):

  def __init__(self):
    pass

  def fit(self, X, y=None):
    return self

  def transform(self, X, y=None): 
    pass
