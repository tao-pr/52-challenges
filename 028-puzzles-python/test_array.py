# Array puzzles

def test_remove_duplicates_sorted():
  ns = [1,2,2,3,1,1,2,3,4,1,2,4,5]

  def remove_dup(vs):
    out = []
    def add_to(v, ws):
      if len(ws)==0:
        return [v]
      elif v<ws[0]:
        return [v]+ws
      elif v>ws[0]:
        return [ws[0]] + add_to(v,ws[1:])
      else:
        return ws

    for v in vs:
      out = add_to(v,out)
    return out

  assert remove_dup(ns) == [1,2,3,4,5]



def test_median_one_pass():
  ns = [4,3,1,5,3,1,2,5,3,1,5]

  def median(vs):
    def add_sorted(v, ws):
      if len(ws)==0:
        return [v]
      elif v<=ws[0]:
        return [v]+ws
      else:
        return [ws[0]]+add_sorted(v,ws[1:])

    sorted_vs = []
    i = 0
    m = 0
    for v in vs:
      sorted_vs = add_sorted(v, sorted_vs)
      # median index steps next every even index
      if i>0 and i%2==0:
        m += 1
      i += 1
    return sorted_vs[m]

  assert median(ns) == 3

