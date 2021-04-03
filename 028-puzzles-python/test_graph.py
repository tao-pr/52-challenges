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
          heappush(Q, (b, new_w)) 
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


def test_reconstruct_itinerary():
  # REF: https://leetcode.com/problems/reconstruct-itinerary/

  def toposort(tickets, n, visited, order):
    # DFS through next airports
    visited.add(n)
    for m in nextFrom(n, tickets):
      if m not in visited:
        toposort(tickets, m, visited, order)
    order.append(n) # Add source airport at the end

  def nextFrom(n, tickets):
    # Suppose `n` always exists in tickets
    nn = []
    for a,b in tickets:
      if a==n:
        nn.append(b)
    return nn

  def findItinerary(tickets):
    from functools import reduce
    # topological sort
    order = []
    nodes = set(reduce(lambda x,y: x+y, [[a,b] for a,b in tickets]))
    visited = set()
    for n in nodes:
      if n not in visited:
        toposort(tickets, n, visited, order)
    return order[::-1]

  assert nextFrom("MUC", [["MUC","LHR"],["JFK","MUC"]]) == ["LHR"]
  assert findItinerary([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]) == \
    ["JFK", "MUC", "LHR", "SFO", "SJC"]

  #assert findItinerary([["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]) == \
  #  ["JFK","ATL","JFK","SFO","ATL","SFO"]

def test_find_prereqs():
  def to_maps(plan):
    pm, rm = {}, {}
    for a,b in plan:
      if a not in pm:
        pm[a] = []
      if b not in rm:
        rm[b] = []
      pm[a].append(b)
      rm[b].append(a)
    return pm, rm

  def find_prereqs(plan, courses):
    plan_map, plan_reverse_map = to_maps(plan)
    order = toposort(plan_map)
    # Cut the topo sort upto the last courses required
    last_course_index = max([order.index(c) for c in courses])
    order = order[:last_course_index+1]
    # Remove courses which are not required 
    out = []
    for a in order:
      if is_required_by_any(a, courses, plan_reverse_map):
        out.append(a)
    return out

  def is_required_by_any(a, courses, plan_reverse_map):
    if a in courses:
      return True
    for c in courses:
      # Check if a required by c
      if c in plan_reverse_map:
        if a in plan_reverse_map[c]:
          return True

        # Check if any of prereqs of c requires a
        return is_required_by_any(a, plan_reverse_map[c], plan_reverse_map)

    return False

  def find_topo_sort(a, plan_map, visited, order):
    # Iterate next nodes from a
    visited.add(a)
    if a in plan_map:
      for b in plan_map[a]:
        # DFS
        if b not in visited:
          find_topo_sort(b, plan_map, visited, order)
    order.append(a)

  def toposort(plan_map):
    visited = set()
    order = []
    for a,b in plan_map.items():
      if a not in visited:
        find_topo_sort(a, plan_map, visited, order)
    return order[::-1]

  plan1 = [
    ['C101', 'C102'],
    ['C102', 'C201'],
    ['C102', 'C301'],
    ['C201', 'C301'],
    ['C203', 'C302'],
    ['C102', 'C203'],
    ['C301', 'C401']
  ]
  assert find_prereqs(plan1, ['C101','C201','C301']) == ['C101','C102','C201','C301']
  assert find_prereqs(plan1, ['C301','C401']) == ['C101','C102','C201','C301','C401']


def test_route_is_bidirectional_cyclic():
  def is_strongly_connected(G):
    nodes = set()
    edgeMap = {}
    edgeReverseMap = {}
    # Create edge map, reverse map
    for a,b in G:
      nodes.add(a)
      nodes.add(b)
      if a not in edgeMap:
        edgeMap[a] = []
      edgeMap[a].append(b)

      if b not in edgeReverseMap:
        edgeReverseMap[b] = []
      edgeReverseMap[b].append(a)

    nodes = list(nodes)
    for i, a in enumerate(nodes):
      for j, b in enumerate(nodes):
        if i==j:
          continue
        visited = set([a])
        if not reachable(edgeMap,a,b,visited):
          return False
        visited = set([a])
        if not reachable(edgeReverseMap,a,b,visited):
          return False
    return True

  def reachable(edgeMap, a, b, visited):
    if a==b:
      return True
    if a in edgeMap:
      if b in edgeMap[a]:
        return True
      # DFS
      for n in edgeMap[a]:
        if n not in visited:
          visited.add(n)
          if reachable(edgeMap, n, b, visited):
            return True
    return False

  G1 = [
    [1,2],[1,3],[1,4],
    [2,1],[2,4]
  ]
  assert is_strongly_connected(G1) == False

  G2 = [
    [1,2],[1,3],[1,4],
    [2,1],[2,4],
    [3,2],
    [4,1]
  ]
  assert is_strongly_connected(G2) == True


def test_find_longest_path_without_repeat():
  # Find longest path in the directed graph without repeating the nodes.
  # Graph is defined with adjacency matrix.
  from heapq import heappush, heappop
  def longest_walk(G):
    H = []
    # DFS
    N = len(G)
    for n in range(N):
      walk(G, [n], H)
    L,W = heappop(H)
    return W

  def walk(G, W, H):
    p = W[-1]
    for a in range(len(G[p])):
      if a!=p and G[p][a]==1 and a not in W:
        Wx = W[:]
        Wx.append(a)
        heappush(H, (-len(Wx), Wx))
        walk(G, Wx, H)

  G1 = [[0,1,0,0,0],
        [0,1,1,0,1],
        [0,1,0,1,1],
        [1,0,0,0,1],
        [0,1,0,1,0]]
  assert longest_walk(G1) == [0,1,2,3,4]

  G2 = [[0,0,0,0],
        [1,0,1,0],
        [1,1,0,1],
        [1,1,0,0]]
  assert longest_walk(G2) == [1,2,3,0]