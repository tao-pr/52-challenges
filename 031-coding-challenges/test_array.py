def test_spiral_walk_matrix():
  """
  Given a matrix M,
  run spiral walk (clockwise, outwards from the inside)
  starting from the specified position (row, col)

  Always go to the right first if possible
  """

  def walk(M, i, j):
    collected = set([(i,j)])
    w = [M[i][j]]
    dr = [[0,1],[1,0],[0,-1],[-1,0]] # right first

    def OOB():
      d = dr[0]
      a,b = i+d[0], j+d[1]
      return not ((0<=a<len(M)) and (0<=b<len(M[0])))

    # rotate direction vector until the next step can be taken
    k = 0
    while k<4 and OOB():
      dr = dr[1:] + [dr[0]]
      k += 1

    w = iterwalk(M, i, j, w, dr, collected)
    return w

  """
  8 9 x x
  7 0 1 2
  6 5 4 3
  """

  def iterwalk(M, i, j, w, dr, collected):
    # step to next cell
    nrows = len(M)
    ncols = len(M[0])
    d = dr[0]
    a, b = i+d[0], j+d[1]
    # collect next cell if in boundary
    can_collected = False
    if (0<=a<nrows) and (0<=b<ncols):
      w.append(M[a][b])
      collected.add((a,b))
      can_collected = True

    # determine next iteration:
    # - keep same direction
    # - change direction
    # - stop
    nextdir = dr[1]
    i, j = a, b
    a, b = a+nextdir[0], b+nextdir[1]
    if (0<=a<nrows) and (0<=b<ncols) and (a,b) not in collected:
      # change direction
      dr = dr[1:] + [dr[0]]
    elif not can_collected:
      # stop, we cannot collect a cell nor change the direction
      return w

    return iterwalk(M, i, j, w, dr, collected)

  M1 = [[1]]
  assert walk(M1, 0, 0) == [1]

  M2 = [
    [1,2,5],
    [3,3,4],
    [0,1,3]
  ]
  assert walk(M2, 1, 1) == [3,4,3,1,0,3,1,2,5]
  assert walk(M2, 1, 2) == [4,3,1,3,2,5]

  M3 = [
    [1,1,2,2],
    [0,1,5,3],
    [1,4,5,7]
  ]
  assert walk(M3, 1, 2) == [5,3,7,5,4,1,1,2,2]


def test_diagonal_walk():
  """
  Given a matrix M,
  create a diagonal walk which 
  0 1 2
  3 4 5

  becomes: 0 1 3 2 4 5
  """
  def diag(M):
    w = []
    """
    0 1 2
    3 4 5
    6 7 8
    """
    return dwalk(M, 0, 0, [])

  def dwalk(M, i, j, w):
    a,b = i,j
    """
    Diagonal walk

    time complexity : O(n*m)
    """
    while a<=len(M)-1 and b>=0: 
      w.append(M[a][b])
      a += 1
      b -= 1

    # all collected
    if i==len(M)-1 and j==len(M[0])-1:
      return w
    # next to the right
    if j<len(M[0])-1:
      j += 1
    else:
      i += 1
    return dwalk(M, i, j, w)

  M = [[1]]
  assert diag(M) == [1]

  M = [
    [2, 3, 4],
    [5 ,6, 7]
  ]
  assert diag(M) == [2, 3, 5, 4, 6, 7]

  M = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
  ]
  assert diag(M) == [1, 2, 4, 3, 5, 7, 6, 8, 9]


def test_find_missing_values():
  """
  Given a array,
  Find all missing integers in between
  """
  def findmissing(ns):
    ms = []
    prev = ns[0]-1
    for n in ns:
      if n-prev>1:
        ms += list(range(prev+1, n))
      prev = n
    return ms

  assert findmissing([1]) == []
  assert findmissing([1,2,3,4,5]) == []
  assert findmissing([1,3,4,5,7,8,9]) == [2,6]
  assert findmissing([1,2,3,8,9,11,12]) == [4,5,6,7,10]

def test_bar():
  """
  Given an array M, each element indicates the height of terrain.
  If we drop a bar of length L,
  find the maximum height which can support this bar

  NOTE: The bar can be stable if both highest supports have the same height
  """
  def highest_support(M, L):
    """
            x
      x     x x     x
    x x x x x x x x x
    """
    from bisect import insort_left
    longest = []
    lopen = {} # opening left supports
    for i,h in enumerate(M):
      if h==0:
        continue
      if h in lopen:
        # there exists opening left support of the same height
        iopen = lopen[h]
        length = i-iopen+1
        if length <= L:
          insort_left(longest, (-length, h))
        del lopen[h]
      else:
        # remove all opening left which are lower than h
        keys = list(filter(lambda k: k<h, lopen.keys()))
        for k in keys:
          del lopen[k]
        # register left opening
        lopen[h] = i

    if len(longest)==0:
      return None
    else:
      _,h = longest[0]
      return h

  assert highest_support([0,1,1,0,0,2,1,0,0,1], 3) == 1
  assert highest_support([0,1,5,3,0,1,5,2], 2) == None
  assert highest_support([0,1,5,3,0,1,5,2], 4) == None
  assert highest_support([0,1,5,3,0,1,5,2], 5) == 5
  assert highest_support([0,1,5,3,0,1,5,2], 7) == 5


def test_create_matrix_from_spiral_walk():
  """
  Given an array of spiral walk starting from (0,0),
  reconstruct a square matrix back
  """
  def to_mat(walk):
    from math import sqrt
    w = int(sqrt(len(walk)))
    M = [[None]*w for i in range(w)]
    
    n = 0
    r,c = 0, 0
    directions = [(0,1),(1,0),(0,-1),(-1,0)]
    while n < w*w:
      M[r][c] = walk[n]
      n += 1

      # next cell
      dr,dc = directions[0]
      if 0<=r+dr<w and 0<=c+dc<w and M[r+dr][c+dc] is None:
        # keep the same direction if still in boundary, or cell not filled yet
        r += dr
        c += dc
      else:
        # change direction if hits boundary, or the cell already filled
        directions = directions[1:] + [directions[0]]
        dr,dc = directions[0]
        r += dr
        c += dc

    return M

  assert to_mat([1]) == [[1]]
  assert to_mat([1,2,3,4]) == [[1,2],[4,3]]
  M = [
    [0,0,0,0,1],
    [3,4,4,4,1],
    [3,5,5,4,1],
    [3,5,5,5,1],
    [3,2,2,2,2]
  ]
  assert to_mat([0]*4+[1]*4+[2]*4+[3]*4+[4]*4+[5]*5) == M


def test_find_max_in_partial_sorted_matrix():
  """
  Given a matrix M which:
    - all elements in the same row are split into 2 parts at k
    - left part, all elements are sorted descendingly: M[_][i] <= M[_][i+1], i<=k
    - right part, all elements are sorted ascendingly: M[_][i] >= M[_][i+1], i>=k
    - split index [i] of each row is not necessarily the same position
  """
  def findm(M):
    mx = M[0][0]
    r,c = 0,0
    # complexity :
    # worst case : O(R * C)
    # best case  : O(R)
    while r<len(M):
      # find pivot position (max)
      while 0 <= c < len(M[r]):
        # x, y, z
        x = M[r][c-1] if c>0 else M[r][c]
        y = M[r][c]
        z = M[r][c+1] if c<len(M[r])-1 else M[r][c]

        if x<=y and y>z:
          # pivot found
          mx = max(mx, y)
          break
        else:
          c += 1

      mx = max(mx, M[r][len(M[r])-1])

      r += 1 # next row
      c = 0 # starting from the left most
    return mx

  M = [
    [1,3,1],
    [0,0,1],
    [1,2,3]
  ]
  assert findm(M) == 3

  M = [
    [1,1,3,5,4,3],
    [0,1,0,0,0,0],
    [1,1,3,2,1,1],
    [0,4,4,5,7,3]
  ]
  assert findm(M) == 7

  M = [[4]]
  assert findm(M) == 4