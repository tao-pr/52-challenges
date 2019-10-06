import numpy as np

from sklearn.pipeline import *
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression

def load_model(path):
  return pickle.load(open(path, 'rb'))

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

  def __init__(self, blueprint: BaseEstimator, output_col: str, split_ratio: float):
    self.model = blueprint
    self.output_col = output_col
    self.split_ratio = split_ratio

  def fit(self, Z, y=None):
    (X,y) = Z

    # Split the dataset into training and testing
    cutoff = int(self.split_ratio * len(X))
    X_train = X[:cutoff]
    X_test = X[cutoff:]
    y_train = y[:cutoff]
    y_test = y[cutoff:]

    print('Training set size : {}'.format(len(X_train)))
    print('Test set size.    : {}'.format(len(X_test)))

    self.model.fit(X_train, y_train)

    print('Running cross validation')
    y_pred = self.model.predict(X_test)

    # Measure mean square error
    rmse = np.sqrt(np.sum(np.square(y_pred) - np.square(y_test)))/float(len(y_pred))
    print('mean square error : {}'.format(rmse))

    return self

  def transform(self, Z, y=None):
    (X,y) = Z
    X[self.output_col] = self.model.predict(X)
    return X


clf = make_pipeline(
    CountryEncoder(input_col='Country', output_col='cnt'),
    ColumnsSelector(),
    Regressor(
      blueprint=LinearRegression(normalize=True, n_jobs=4),
      output_col='pred_temp_change',
      split_ratio=0.85)
    )
