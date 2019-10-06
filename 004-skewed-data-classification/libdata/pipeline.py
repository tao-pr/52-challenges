from sklearn.pipeline import *
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

clf = make_pipeline(
  memory=None,
  steps=[
    ('CountryEncoder', CountryEncoder(input_col='Country', output_col='cnt')),
    ('FeatureSelector', ColumnsSelector()),
    ('Regressor', Regressor(blueprint=LinearRegression(
      normalize=True, n_jobs=4)))
    ])

class ColumnsSelector(BaseEstimator, TransformerMixin):
  """
  Columns selector split dataframe into X, y
  """
  
  def __init__(self):
    pass

  def fit(self, X, y=None):
    return self

  def transform(self, X, y=None) -> (np.ndarray, np.ndarray): 
    return (X[['cnt','year','month','prev_month','temp_prev','lat','lng']],
            X[['temp_change']])


class CountryEncoder(BaseEstimator, TransformerMixin):

  def __init__(self, input_col: str, output_col: str):
    self.input_col = input_col
    self.output_col = output_col

  def fit(self, X, y=None):
    self.encoder = LabelEncoder()
    self.encoder.fit(X[self.input_col])
    return self

  def transform(self, X, y=None): 
    X[self.output_col] = self.encoder.transform(X[self.input_col])
    return X


class Regressor(BaseEstimator, TransformerMixin):

  def __init__(self, blueprint: BaseEstimator):
    self.model = blueprint

  def fit(self, X, y=None):
    pass

  def transform(self, X, y=None):
    pass

