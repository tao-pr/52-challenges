module Sample
  ( Point(..),
    genPar,
    foldCount
  )
  where

import Control.Parallel.Strategies
import GHC.Base(returnIO)
import System.Random

data Point = Point Float Float 
  deriving Show


genPar :: Int -> [IO Point]
genPar num = map gen [1..num]

gen :: Int -> IO Point
gen _ = do 
    a <- getStdRandom (randomR (-1, 1)) :: IO Float
    b <- getStdRandom (randomR (-1, 1)) :: IO Float
    let p = Point a b
    return p

foldCount :: (Point -> Bool) -> (Int, Int) -> [Point] -> (Int, Int)
foldCount predicate (a0, b0) [] = (a0, b0)
foldCount predicate (a0, b0) (x:xs) = 
  foldCount predicate ab xs
    where
      ab = if predicate x 
      then (a0+1, b0)
      else (a0, b0+1)