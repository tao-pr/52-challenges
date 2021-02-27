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

