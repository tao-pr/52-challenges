module Sample where

import Data.Geometry.Point (Point, Point(Point2))

class Sample s where
  inScope :: s a -> Bool
  gen :: s a -- generate a sample
  genPar :: Int -> [s a] -- generate multiple samples in parallel

instance Sample (Point p) where
  inScope p = error ""
  gen = error ""
  genPar = error ""



