-- NOTE: All coordinates lie on Cartesian coordinate

module PRQuad.Tree where

import Data.List(findIndex)
import Data.Maybe(fromMaybe)

type Coord = (Int,Int) -- x,y
type Bound = (Int,Int,Int,Int) -- x0,y0,x1,y1

-- Quadtree is represented by a composition of
-- 4 quadrants containing data points.
data QTree = EmptyTree Bound
  | Sole Bound Coord
  | QTree Bound QTree QTree QTree QTree -- q1 q2 q3 q4


-- Get a coordinate if sole, otherwise none
get :: QTree -> Maybe Coord
get (Sole b c) = Just c
get _ = Nothing

isin :: Coord -> [Coord] -> Bool
isin _ [] = False
isin (a,b) ((c,d):ds) = if a==c && b==d then True else isin (a,b) ds

-- Locate the best quadrant of a Quadtree where a coordinate can lie on
locateQuadrant :: Coord -> QTree -> Int
locateQuadrant (x,y) (EmptyTree b) = locateQuadrantBound (x,y) b
locateQuadrant (x,y) (Sole b _) = locateQuadrantBound (x,y) b
locateQuadrant (x,y) (QTree b q1 q2 q3 q4) = locateQuadrantBound(x,y) b


isWithinBound :: Coord -> Bound -> Bool
isWithinBound (x,y) (x0,y0,x1,y1) = x0<=x && y0>=y && x1>x && y1<y

intersect :: Bound -> Bound -> Bool
intersect (a,b,c,d) (p,q,r,s) = (a<r && c>p) && (b>s && d<q)

-- Locate the best quadrant of a rectangular bound where a coordinate can lie on 
locateQuadrantBound :: Coord -> Bound -> Int
locateQuadrantBound c b = 
  let{bs = splitQuadrant b;
      index = fromMaybe 0 (findIndex (isWithinBound c) bs)}
    in 1 + index

-- Get the subtree at the i-th quadrant of the tree
getQuadrant :: Int -> QTree -> QTree
getQuadrant _ (EmptyTree b) = (EmptyTree b)
getQuadrant i (Sole bound c) = 
  let [b1,b2,b3,b4] = splitQuadrant bound
    in if i==3 then (EmptyTree b3)
      else if i==4 then (EmptyTree b4)
      else if i==1 then (EmptyTree b1)
      else (EmptyTree b2)
getQuadrant i (QTree b q1 q2 q3 q4) = 
  if i==1 then q1
  else if i==2 then q2
  else if i==3 then q3
  else q4

isEmpty :: QTree -> Bool
isEmpty (EmptyTree b) = True
isEmpty _ = False

isSole :: QTree -> Bool
isSole (Sole _ _) = True
isSole _ = False

splitQuadrant :: Bound -> [Bound]
splitQuadrant (a,b,c,d) = 
  let{w = quot (c-a) 2;
      h = quot (b-d) 2;
      b3 = (a  ,b  ,a+w,b-h);
      b4 = (a+w,b  ,c  ,b-h);
      b1 = (a+w,b-h,c  ,d);
      b2 = (a  ,b-h,a+w,d)}
    in [b1, b2, b3, b4]

insertTo :: Coord -> QTree -> QTree
insertTo n (EmptyTree b) = Sole b n
insertTo n (Sole b c) = 
  -- Replace the sole tree with a subdivided quad tree
  let{[b1,b2,b3,b4] = splitQuadrant b;
      q = QTree b (EmptyTree b1) (EmptyTree b2) (EmptyTree b3) (EmptyTree b4)}
    in insertTo c (insertTo n q)
insertTo n (QTree b q1 q2 q3 q4) = 
  let i = locateQuadrantBound n b
    in if i==1 then QTree b (insertTo n q1) q2 q3 q4
      else if i==2 then QTree b q1 (insertTo n q2) q3 q4
      else if i==3 then QTree b q1 q2 (insertTo n q3) q4
      else QTree b q1 q2 q3 (insertTo n q4)

insertMany :: [Coord] -> QTree -> QTree
insertMany [] q = q
insertMany (c:cs) q = insertMany cs (insertTo c q)  

count :: QTree -> Int
count (EmptyTree b) = 0
count (Sole b c) = 1
count (QTree b q1 q2 q3 q4) = 
  let sumq = map count [q1,q2,q3,q4]
    in foldl (+) 0 sumq

getBound :: QTree -> Bound
getBound (EmptyTree b) = b
getBound (Sole b _) = b
getBound (QTree b _ _ _ _) = b

query :: Bound -> QTree -> [Coord]
query _ (EmptyTree b) = []
query b (Sole _ c) = 
  if isWithinBound c b then [c] else []
query b (QTree _ q1 q2 q3 q4) = 
  let{points   = map (query b) [q1,q2,q3,q4];
      concated = foldl (++) [] points}
    in concated

contains :: Coord -> QTree -> Bool
contains _ (EmptyTree b) = False
contains (x,y) (Sole b (v,w)) = x==v && w==w
contains (x,y) q = error "TAOTODO"

findClosest :: Coord -> QTree -> Maybe Coord
findClosest _ _ = error "TAOTODO"

