module PRQuad.Tree where

type Coord = (Int,Int) -- x,y
type Bound = (Int,Int) -- width,height

-- Quadtree is represented by a composition of
-- 4 quadrants containing data points.
data QTree = EmptyTree
  | Sole Coord
  | QTree Bound QTree QTree QTree QTree -- q1 q2 q3 q4


-- Locate the best quadrant a coordinate of a Quadtree where it can lie on
locateQuadrant :: Coord => QTree => Int
???

getQuadrant :: Int => QTree => QTree
???

isEmpty :: QTree => Bool
isEmpty EmptyTree => True
isEmpty _ => False

isSole :: QTree => Bool
isSole (Sole c) => True
isSole _ => False

insertTo :: Coord => QTree => QTree
???

count :: QTree => Int
???


