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



def test_can_we_install_these_orders():

  def find_order_install(g, orders):
    from functools import reduce
    nodes = list(set(reduce(lambda x,y: x+y, [[a,b] for a,b in g])))
    req = toposort(g, nodes)
    verify = []
    for a,b in orders:
      verify.append(req.index(a)<req.index(b))
    return verify

  def topoSearch(n, g, visited, stack):
    if n not in stack:
      # Traverse next vertices from n
      for a, b in g:
        if a==n and b not in visited:
          visited.add(b)
          topoSearch(b, g, visited, stack)
      stack.append(n)

  def toposort(g, nodes):
    visited = set()
    stack = []
    for n in nodes:
      if n not in visited:
        visited.add(n)
        topoSearch(n, g, visited, stack)
    return stack[::-1]

  g1 = [
    [1,0], # u->v means, u is prequisite of v
    [2,0],
    [0,3],
    [2,4],
    [0,4]
  ]
  assert toposort(g1, [0,1,2,3,4]) == [2,1,0,4,3]
  assert find_order_install(g1, [[0,1],[1,4],[1,3]]) == [False, True, True]


def test_find_min_cost_to_reach_goal():
  from heapq import heappush, heappop
  from functools import reduce

  def min_cost_to_goal(G, start, finish):
    prev = dijkstra(G, start, finish)

    # Backtrack from finish to start, accumulate weight
    w = 0
    b = finish
    while b != start:
      b_ = prev[b]
      w += get_weight(G, b_, b)
      b = b_
    return w

  def get_path(G, start, finish):
    prev = dijkstra(G, start, finish)
    # Backtrack from finish to start, accumulate weight
    w = 0
    b = finish
    path = [finish]
    while b != start:
      b = prev[b]
      path.append(b)
    return path[::-1]

  def get_weight(G, a, b):
    for i,j,w in G:
      if i==a and b==j:
        return w
    return float('inf')

  def dijkstra(G, start, finish):
    nodes = set(reduce(lambda x,y: x+y, [[a,b] for a,b,w in G]))
    Q = [] # heap: (weight, node)
    H = {}
    prev = {}
    for a in nodes:
      if a == start:
        heappush(Q, (a, 0))
        H[a] = 0
      else:
        H[a] = float('inf')

    # Iterate
    while len(Q)>0:
      (a,wa) = heappop(Q)
      for b,wb in adj(G,a):
        if H[b] > wb:
          # update new weight of [b]
          new_w = wa + wb
          H[b] = new_w
          prev[b] = a
          # add b back to q
          heappush(Q, (b, new_w)) # TAOTODO?
    return prev

  def adj(G, a):
    return [(j,w) for i,j,w in G if i==a]

  g1 = [ # a -> b , weight
    [0,1,14],
    [0,2,25],
    [0,3,1],
    [1,2,10],
    [2,3,10],
    [2,4,25],
    [3,4,100]
  ]
  assert get_path(g1, 0, 4) == [0,1,2,4]
  assert min_cost_to_goal(g1, 0, 4) == 49