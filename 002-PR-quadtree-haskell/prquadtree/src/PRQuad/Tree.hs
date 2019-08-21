module PRQuad.Tree where

type Coord = (Int,Int) deriving Show -- x,y
type Bound = (Int,Int,Int,Int) deriving Show -- x0,y0,x1,y1

-- Quadtree is represented by a composition of
-- 4 quadrants containing data points.
data QTree = EmptyTree Bound
  | Sole Bound Coord
  | QTree Bound QTree QTree QTree QTree -- q1 q2 q3 q4


-- Locate the best quadrant of a Quadtree where a coordinate can lie on
locateQuadrant :: Coord => QTree => Int
???

-- Locate the best quadrant of a rectangular bound where a coordinate can lie on 
locateQuadrantBound :: Coord => Bound => Int
locateQuadrant (x,y) (x0,y0,x1,y1) = ???

getQuadrant :: Int => QTree => QTree
???


isEmpty :: QTree => Bool
isEmpty EmptyTree _ => True
isEmpty _ => False

isSole :: QTree => Bool
isSole (Sole _ _) => True
isSole _ => False

insertTo :: Coord => QTree => QTree
???

count :: QTree => Int
???

findClosest :: Coord => QTree => Maybe Coord
???

