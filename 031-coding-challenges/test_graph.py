def test_longest_increasing_path():
  """
  Given a matrix M,
  find the longest path (no repeat) which each step 
  keeps the element value increasing
  """
  from heapq import heapify, heappush

  def lip(M):
    # DFS
    P = []
    nrows = len(M)
    ncols = len(M[0])
    for r in range(nrows):
      for c in range(ncols):
        heappush(P, (-1,[(r,c)]))
        dfs(M, [(r,c)], P)
    if len(P)==0:
      return None
    else:
      # reconstruct path values from coordinates
      paths = [M[a][b] for a,b in P[0][1]]
      return paths

  def dfs(M, path, P):
    # Expand next blocks
    a,b = path[-1]
    for i in [-1,0,1]:
      for j in [-1,0,1]:
        # Next block is increasing?
        if 0<=a+i<len(M) and 0<=b+j<len(M[0]):
          if i+j!=0 and ((a+i,b+j) not in path) and (M[a][b] < M[a+i][b+j]):
            p = path + [(a+i,b+j)]
            dfs(M, p, P)
            if len(P)==0 or len(p) > -P[0][0]:
              heappush(P, (-len(p),p))

  M = [[1]]
  assert lip(M) == [1]

  M = [
    [1,4,5],
    [1,3,2],
    [0,1,5]
  ]
  assert lip(M) == [0,1,3,4,5]

  M = [
    [0,1,1,5,6],
    [0,1,1,5,3],
    [0,0,0,1,3],
    [1,3,4,5,7]
  ]
  assert lip(M) == [0,1,3,4,5,7]


