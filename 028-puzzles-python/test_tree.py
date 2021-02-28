class TreeNode: 
  def __init__(self,key): 
    self.left = None
    self.right = None
    self.val = key 


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
    view, level = get_right_view(tree, from_level=0, current_level=0)
    return view

  def get_right_view(tree, from_level, current_level):
    vec = []
    if from_level==current_level:
      vec.append(tree.val)
    
    depth_right = current_level+1
    depth_left = current_level+1

    # DFS right node
    if tree.right is not None:
      subvec, depth_right = get_right_view(
        tree.right, 
        from_level=current_level+1,
        current_level=current_level+1)
      vec = vec + subvec
    if tree.left is not None:
      subvec, depth_left = get_right_view(
        tree.left,
        from_level=depth_right,
        current_level=current_level+1)
      vec = vec + subvec
    return vec, max(depth_right, depth_left)


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
