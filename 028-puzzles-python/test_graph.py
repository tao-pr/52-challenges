from typing import List

def test_map_highest_peak():
  # REF: https://leetcode.com/problems/map-of-highest-peak/

  # Maximise the highest cell while
  # max height diff between 2 adjacent cells is 1
  def highestPeak(isWater: List[List[int]]) -> List[List[int]]:
    # init: zeros represent water
    #       nones represent land (unassigned height)
    H = [[0 if c==1 else None for c in row] for row in isWater]
    num_filled = sum([c for row in isWater for c in row])

    # 1 | 1 | 0
    # 0 | 1 | 1
    # 0 | 1 | 2
    min_value = 0
    while num_filled < len(H)*len(H[0]):
      for i,row in enumerate(H):
        for j,cell in enumerate(row):
          if cell==None:
            # check if cell (i,j) is next to min_value so far?
            if has_adj_of_value(i, j, H, min_value):
              # if so, assign it with [min_value+1]
              H[i][j] = min_value+1
              num_filled += 1
      min_value += 1
    return H

  def has_adj_of_value(row, col, H, value):
    for (i,j) in [[-1,0],[1,0],[0,1],[0,-1]]:
      if row+i>=0 and row+i<len(H) and col+j>=0 and col+j<len(H[0]):
        if H[row+i][col+j] == value:
          return True
    return False

  def min_adjacent_value(row, col, H):
    mv = 0
    for i in [row-1, row, row+1]:
      for j in [col-1, col, col+1]:
        if i!=j and i>=0 and j>=0 and i<len(H) and j<len(H[0]):
          mv = min(mv, H[i][j])
    return mv

  assert highestPeak([[0,1],[0,0]]) == [[1,0],[2,1]]
  assert highestPeak([[0,0,1],[1,0,0],[0,0,0]]) == [[1,1,0],[0,1,1],[1,2,2]]


def test_possible_biparties():
  # REF: https://leetcode.com/problems/possible-bipartition/
  def possibleBipartition(N: int, dislikes: List[List[int]]) -> bool:
    # greedy
    A = set()
    B = set()
    # create reverse map (key is disliked by its member set)
    hate = {}
    for d in dislikes:
      [x,y] = d
      if y not in hate:
        hate[y] = set()
      hate[y].add(x)

    print(hate)

    for i in range(1,N+1):
      # Try to add i => A,
      # If fails, i => B
      # Otherwise, we fail to create biparties
      if not addTo(i, A, hate):
        if not addTo(i, B, hate):
          return False

    return True

  def addTo(i, grp, hate):
    if i in grp:
      return True
    # Do not add if someone in grp hates i
    if i in hate:
      for g in grp:
        if g in hate[i]:
          return False
    grp.add(i)
    return True
  
  assert possibleBipartition(4, [[1,2],[1,3],[2,4]]) == True
  assert possibleBipartition(3, [[1,2],[1,3],[2,3]]) == False
  assert possibleBipartition(4, [[1,2],[1,3],[1,4],[2,3],[1,2]]) == False

