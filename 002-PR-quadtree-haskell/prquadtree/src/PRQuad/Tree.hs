module PRQuad.Tree where

-- Quadtree is represented by a composition of
-- 4 quadrants containing data points.
data QTree a = QTree (QTree a) (QTree a) (QTree a) (QTree a) 
  | EmptyTree

q1 :: QTree a -> QTree a 
q1 EmptyTree = EmptyTree
q1 (QTree b _ _ _) = b

q2 :: QTree a -> QTree a 
q2 EmptyTree = EmptyTree
q2 (QTree _ b _ _) = b

q3 :: QTree a -> QTree a 
q3 EmptyTree = EmptyTree
q3 (QTree _ _ b _) = b

q4 :: QTree a -> QTree a 
q4 EmptyTree = EmptyTree
q4 (QTree _ _ _ b) = b

