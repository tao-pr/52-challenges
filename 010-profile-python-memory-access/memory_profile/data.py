import numpy as np

class M:
  def __init__(self):
    self.data = [np.arange(1,5000) for i in range(1000)]

  def update(self):
    self.data = [v*-1 for v in self.data]
    return self


class Deep:
  def __init__(self):
    self.a = [np.arange(1,5000) for i in range(1000)]
    self.d = {"key": M()}