from functools import reduce

def test_find_longest_sequence():
  """
  Given an array L,
  find the position p and length k which 
    - all elements to the left of p from p-k position are in ascending order
    - all elements to the right of p until p+k position are in descending order
    - and L[p] is the biggest among that sequence 
  """
  def find(L):
    ans = (0,0)
    # Complexity: O(l + m*n)
    # l = length of array
    # m = total length of subsequences (summed), m < l
    # n = number of subsequences, n < l

    for i,p in enumerate(L):
      ansp = expand(L, p, p, i, 1)
      # update answer if a longer sequence is found
      if ansp[1] > ans[1]: 
        ans = ansp
    return ans

  def expand(L, pleft, pright, i, k):
    if i-k>=0 and i+k<len(L) and L[i-k] < pleft and L[i+k] < pright:
      return expand(L, L[i-k], L[i+k], i, k+1)
    else:
      return (i,k-1) # Recede

  assert find([0,1,0]) == (1,1)
  assert find([4,3,2,5,6,3,2,1]) == (4,2)
  assert find([2,4,3,2,1,2,3,4,5]) == (1,1)


def test_count_num_of_rectangles():
  """
  Given a set of points on 2d coordinates,
  find how many right rectangles we can connect those dots
  """
  def count_rect(ps):
    # create hashmap of all points : Y -> X
    # Complexity : O(p)
    from bisect import insort_left
    ymap = {}
    for x,y in ps:
      if y not in ymap:
        ymap[y] = [x]
      else:
        insort_left(ymap[y], x) # keep them sorted
    
    # Connect horizontal lines 
    # Complexity : O(y), y<=p
    hlines = {}
    for y in ymap.keys():
      # Generate combination of x pos 
      hlines[y] = []
      for i,x1 in enumerate(ymap[y]):
        for x2 in ymap[y][i+1:]:
          hlines[y].append((x1,x2))

    # Identify matching parallel lines
    # Complexity : O(y^2 * x)
    nrect = 0
    hkeys = list(hlines.keys())
    for i,y1 in enumerate(hkeys):
      for x1,x2 in hlines[y1]:
        # we must look for other horizontal lines with the same begin & end
        for y2 in hkeys[i+1:]:
          for x1_,x2_ in hlines[y2]:
            if x1==x1_ and x2==x2_:
              # vertical lines matched!
              nrect += 1
    return nrect

  ps = [(0,0), (0,1), (1,0), (1,1)]
  assert count_rect(ps) == 1

  ps = [(0,5), (5,0)]
  assert count_rect(ps) == 0

  ps = [(0,0), (0,1), 
        (1,0), (1,1), (1,2), (1,5),
        (2,0),        (2,2)]
  assert count_rect(ps) == 2

  ps = [(0,0), (0,1), 
        (1,0), (1,1), (1,2), (1,5),
        (2,0), (2,1),        (2,5)]
  assert count_rect(ps) == 5


def test_min_coins():
  """
  Given a set of coins, eg [5,5,2,1, 0.25]
  find the combination which can pay for a product at specified price
  which leaves minimal "number" of coins left in the pocket
  """
  def getbest(a,b):
    return a if len(a)>len(b) else b

  def min_coins(coins, price, pre=[], best=[]):
    # greedy algorithm
    for i,c in enumerate(coins):
      if c==price: 
        # last coin
        best = getbest(pre+[c], best)
      else:
        # generate tail combination
        tail = coins[:i] + coins[i+1:]
        if len(tail)==0:
          # no way to sum up to price
          continue
        else:
          best = getbest(min_coins(tail, price-c, pre=pre+[c], best=best), best)
    return best

  assert min_coins([10,5,5,5,1,1], 12) == [5,5,1,1] # 2 coins left
  assert min_coins([5,5,2,1,0.5,0.5], 7) == [5,1,0.5,0.5] # 2 coins left
  assert min_coins([2,2,2,1,0.5,0.25,0.25], 5) == [2,2,0.5,0.25,0.25] # 2 coins left


def test_pair_tasks():
  """
  Given a list of people with maximum capacity
  and a list of tasks with amount of effort,

  pair people with tasks, such that:
    - everyone has at least 1 task to do
    - all tasks are assigned
    - no one takes more tasks than their capacity
    - a task cannot be assigned to more than 1 people
    - no one takes more than 3 tasks
  """
  def assign(pp, tasks):
    # greedy, assign heavy tasks first
    # sort complexity : O(Tlog(T))
    tasks = sorted(tasks, reverse=True)
    return gassign(pp[:], tasks, [[] for _ in pp])

  def gassign(pp, tasks, assigned):
    # complexity : O(T * P)
    for t in tasks:
      for i in range(len(pp)):
        if pp[i]>=t and len(assigned[i])<3:
          pp[i] -= t
          assigned[i].append(t)
          break
    return assigned


  def is_valid(assigned, pp, tasks):
    print(f'pp = {pp}')
    print(f'tasks = {tasks}')
    print(f'assigned = {assigned}')
    assert sorted(tasks) == sorted(reduce(lambda a,b: a+b, assigned))
    assert len(assigned) == len(pp)
    for p,t in zip(pp, assigned):
      assert p>=sum(t)

  # 1 -> 1
  # 3 -> 1,1,1
  # 2 -> 1,1
  # 4 -> 3,1
  pp = [1,3,2,4]
  tasks = [1,1,1,1,1,1,3]
  is_valid(assign(pp, tasks), pp, tasks)
  # 5 -> 1,1,4
  # 4 -> 2,2
  # 1 -> 1
  # 3 -> 2,1
  pp = [5,4,1,3]
  tasks = [1,2,1,4,2,1,2]
  is_valid(assign(pp, tasks), pp, tasks)
  # 6 -> 4,1
  # 3 -> 1,1,1
  pp = [6,3]
  tasks = [4,1,1,1,1]
  is_valid(assign(pp, tasks), pp, tasks)
