# BST 
class TreeNode: 
  def __init__(self,key): 
    self.left = None
    self.right = None
    self.val = key 


# For Facebook's query
class Node: 
  def __init__(self, data): 
    self.val = data 
    self.children = []


def test_count_visible__left_nodes():
  def visible_nodes(root):
    # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=495004218121393
    # 
    # hint: leftmost node on each level may be right node

    num_visible_left = 0
    num_visible_right = 0
    if root.left is not None:
      num_visible_left = visible_nodes(root.left)
    if root.right is not None:
      num_visible_right = visible_nodes(root.right)
    return 1+max(num_visible_left, num_visible_right)


  # Test
  root_1 = TreeNode(8)
  root_1.left = TreeNode(3)
  root_1.right = TreeNode(10)
  root_1.left.left = TreeNode(1)
  root_1.left.right = TreeNode(6)
  root_1.left.right.left = TreeNode(4)
  root_1.left.right.right = TreeNode(7)
  root_1.right.right = TreeNode(14)
  root_1.right.right.left = TreeNode(13)
  assert visible_nodes(root_1) == 4

  root_2 = TreeNode(10)
  root_2.left = TreeNode(8)
  root_2.right = TreeNode(15)
  root_2.left.left = TreeNode(4)
  root_2.left.left.right = TreeNode(5)
  root_2.left.left.right.right = TreeNode(6)
  root_2.right.left =TreeNode(14)
  root_2.right.right = TreeNode(16)
  assert visible_nodes(root_2) == 5


def test_flatten_tree_to_list():
  # REF: https://leetcode.com/problems/flatten-binary-tree-to-linked-list/
  def flatten(tree):
    vec = [tree.val]
    if tree.left is not None:
      vec = flatten(tree.left) + vec
    if tree.right is not None:
      vec = vec + flatten(tree.right)
    return vec



  # Test
  #             8
  #           /   \
  #          3     10
  #         / \      \    
  #        1   6     14
  #           / \    /
  #          4   7  13
  root_1 = TreeNode(8)
  root_1.left = TreeNode(3)
  root_1.right = TreeNode(10)
  root_1.left.left = TreeNode(1)
  root_1.left.right = TreeNode(6)
  root_1.left.right.left = TreeNode(4)
  root_1.left.right.right = TreeNode(7)
  root_1.right.right = TreeNode(14)
  root_1.right.right.left = TreeNode(13)
  assert flatten(root_1) == [1,3,4,6,7,8,10,13,14]


def test_right_side_view():
  # REF: https://leetcode.com/problems/binary-tree-right-side-view/
  def right_view(tree):
    vec = []
    proj = project_right(tree, weight=1, current_depth=0, proj={})
    for level, node in proj.items():
      w,val = node
      vec.append(val)
    return vec

  def project_right(tree, weight, current_depth, proj):
    if current_depth not in proj:
      proj[current_depth] = (weight, tree.val)
    else:
      w,a = proj[current_depth]
      if weight>w:
        proj[current_depth] = (weight, tree.val)

    # DFS to right first
    if tree.right is not None:
      proj = project_right(tree.right, weight<<1, current_depth+1, proj) 

    # DFS to left afterwards
    if tree.left is not None:
      proj = project_right(tree.left, weight, current_depth+1, proj)

    return proj

  # Test
  #             8
  #           /   \
  #          3     10
  #         / \      \    
  #        1   6     14
  #           / \    /
  #          4   7  13
  root_1 = TreeNode(8)
  root_1.left = TreeNode(3)
  root_1.right = TreeNode(10)
  root_1.left.left = TreeNode(1)
  root_1.left.right = TreeNode(6)
  root_1.left.right.left = TreeNode(4)
  root_1.left.right.right = TreeNode(7)
  root_1.right.right = TreeNode(14)
  root_1.right.right.left = TreeNode(13)
  assert right_view(root_1) == [8,10,14,13]

  # Test
  #             10
  #            /  \
  #           8    15
  #          /    /  \
  #         4    14   16
  #          \
  #           5
  #            \
  #             6
  root_2 = TreeNode(10)
  root_2.left = TreeNode(8)
  root_2.right = TreeNode(15)
  root_2.left.left = TreeNode(4)
  root_2.left.left.right = TreeNode(5)
  root_2.left.left.right.right = TreeNode(6)
  root_2.right.left =TreeNode(14)
  root_2.right.right = TreeNode(16)
  assert right_view(root_2) == [10,15,16,5,6]


def test_count_char_nodes():
  # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=3068294883205371

  #           1(a)
  #         /   \
  #       2(b)  3(a)

  # s = "aba"
  # RootNode = 1
  # query = [[1, 'a']]  ==> output = [2]

  # Note: 
  # Node 1 corresponds to first letter 'a', 
  # Node 2 corresponds to second letter of the string 'b', 
  # Node 3 corresponds to third letter of the string 'a'.

  # Both Node 1 and Node 3 contain 'a', 
  # so the number of nodes within the subtree of Node 1 containing 'a' 
  # is 2.

  
  def count_of_nodes(root, queries, s):
    ans = []
    for q in queries:
      ans.append(query(root, q, s))
    return ans

  def query(root, query, s):
    u,c = query
    # Find all possible 'val' of [c] in [s]
    vals = [i+1 for k,i in zip(s,range(len(s))) if k==c]
    print(vals)
    return find_in_tree(root, u, vals)

  def find_in_tree(root, u, vals):
    # Locate children of value=u and start finding from its subtrees
    if root.val==u:
      return find_in_subtree(root, vals)
    else:
      ans = 0
      for child in root.children:
        ans += find_in_tree(child, u, vals)
      return ans

  def find_in_subtree(root, vals):
    # Also count root itself if it's the right value we're looking for
    ans = 1 if root.val in vals else 0
    for child in root.children:
      if child.val in vals:
        ans += 1
      # Dig deeper too
      for grandchild in child.children:
        ans += find_in_subtree(grandchild, vals)
    return ans

  # Testcase 1
  n_1 ,q_1 = 3, 1 
  s_1 = "aba"
  root_1 = Node(1) 
  root_1.children.append(Node(2)) 
  root_1.children.append(Node(3)) 
  queries_1 = [(1, 'a')]

  output_1 = count_of_nodes(root_1, queries_1, s_1)
  expected_1 = [2]
  assert expected_1 == output_1

  # Testcase 2
  n_2 ,q_2 = 7, 3 
  s_2 = "abaacab"
  root_2 = Node(1)
  root_2.children.append(Node(2))
  root_2.children.append(Node(3))
  root_2.children.append(Node(7))
  root_2.children[0].children.append(Node(4))
  root_2.children[0].children.append(Node(5))
  root_2.children[1].children.append(Node(6))
  queries_2 = [(1, 'a'),(2, 'b'),(3, 'a')]
  output_2 = count_of_nodes(root_2, queries_2, s_2)
  expected_2 = [4, 1, 2]
  assert expected_2 == output_2


def test_heapsort_array():
  def heapsort(arr):
    # heap sort basically heapifies "all parent nodes"
    # bottom-up direction
    last_node = len(arr)-1
    parent_of_last = (last_node-1)//2

    # build min-heap
    for i in range(parent_of_last, -1, -1):
      heapify(arr, i)

    # Keep popping root out, 
    # swap last node in, until empty tree
    out = []
    while len(arr)>0:
      out.append(arr[0]) # pop root
      arr[0] = arr[len(arr)-1]
      arr = arr[:-1]
      if len(arr)>1:
        # heapify parent nodes
        N = ((len(arr)-1)-1) // 2
        for j in range(N, -1, -1):
          heapify(arr, j)
    arr = out
    return out

  def heapify(arr, root_index=0):
    parent_of_root = (root_index-1)//2
    child_left = root_index*2 + 1
    child_right = root_index*2 + 2
    # swap smallest to the root
    smallest_index = root_index
    if child_left < len(arr) and arr[child_left] < arr[root_index]:
      smallest_index = child_left
    if child_right < len(arr) and arr[child_right] < arr[root_index]:
      smallest_index = child_right
    if smallest_index != root_index:
      # swap
      arr[smallest_index], arr[root_index] = arr[root_index], arr[smallest_index]
    # heapify the root again (if swapped)
    if smallest_index != root_index:
      heapify(arr, root_index)
    return arr

  assert heapify([5,2],0) == [2,5]
  assert heapsort([1,15,3,9,4]) == [1,3,4,9,15]
  assert heapsort([1,8,1,3]) == [1,1,3,8]


def test_largest_triple_products():
  # REF: https://www.facebookrecruiting.com/portal/coding_practice_question/?problem_id=510655302929581
  # Supposed to be 'heap'

  def findMaxProduct(arr):
    from functools import reduce
    from heapq import heapify, heappop, heappush, nlargest
    prod = []
    h = [] # heap
    for i in range(len(arr)):
      # Push i-th element to heap
      heappush(h, arr[i]) 
      if i<2:
        prod.append(-1)
        continue
      
      # Get 3 largest elements
      triplet = nlargest(3, h)
      prod.append(reduce(lambda a,b: a*b, triplet))
    return prod

  arr_1 = [1, 2, 3, 4, 5]
  expected_1 = [-1, -1, 6, 24, 60]
  output_1 = findMaxProduct(arr_1)
  assert expected_1 == output_1

  arr_2 = [2, 4, 7, 1, 5, 3]
  expected_2 = [-1, -1, 56, 56, 140, 140]
  output_2 = findMaxProduct(arr_2)
  assert expected_2 == output_2


def test_kd_tree():
  """
  Implement KD-Tree which has following methods
  - Find N closest points
  - Query all points which have x<?, or y>?
  """
  class KDN:
    def __init__(self, x, y, level=0):
      self.x = x
      self.y = y
      self.left = None
      self.right = None
      self.level = level

    def add(self, x, y):
      if self.level % 2==0:
        isleft = x<=self.x
      else:
        isleft = y<=self.y

      if isleft:
        if self.left is None:
          self.left = KDN(x,y)
        else:
          self.left.add(x,y)
      else:
        if self.right is None:
          self.right = KDN(x,y)
        else:
          self.right.add(x,y)

    def nn(self, k, x, y):
      # BFS locate bounding box which contains the 
      from heapq import heappush, heappop
      H = []
      self._nn(k, x, y, H)
      Q = []
      while len(Q)<k and len(H)>0:
        _, p = heappop(H)
        Q.append(p)
      return Q

    def dist(self, x, y):
      import numpy as np
      p1 = np.array([x,y])
      p2 = np.array([self.x, self.y])
      return np.linalg.norm(p1-p2)

    def _nn(self, k, x, y, H):
      from heapq import heappush, heappop
      R = 10
      d = self.dist(x,y)
      if d<=R:
        heappush(H, (d, (self.x, self.y)))
        # if partition point is in range,
        # also include both children in search
        if self.left is not None:
          self.left._nn(k, x, y, H)
        if self.right is not None:
          self.right._nn(k, x, y, H)
      else:
        # partition point is outside of range,
        # only traverse into one side
        if self.level%2==0:
          # x
          if self.x >= x and self.left is not None:
            self.left._nn(k, x, y, H)
          elif self.x < x and self.right is not None:
            self.right._nn(k, x, y, H)
        else:
          # y
          if self.y >= y and self.left is not None:
            self.left._nn(k, x, y, H)
          elif self.y < y and self.right is not None:
            self.right._nn(k, x, y, H)

  def make_kdn(arr):
    kdn = KDN(arr[0].x, arr[0].y)
    for p in arr[1:]:
      kdn.add(p.x, p.y)
    return kdn

  from collections import namedtuple
  P = namedtuple('P', ['x','y'])

  kdn1 = make_kdn([P(x=3, y=4), P(x=10, y=15), P(x=10, y=12), P(x=6, y=0)])
  assert kdn1.nn(k=1, x=5, y=1) == [(6,0)]
  assert kdn1.nn(k=2, x=5, y=1) == [(6,0),(3,4)]