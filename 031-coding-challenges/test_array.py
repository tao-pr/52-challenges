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
