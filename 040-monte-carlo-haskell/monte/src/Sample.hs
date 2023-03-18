module Sample where

import Control.Parallel.Strategies
import GHC.Base(returnIO)
import System.Random

data Point = Point Float Float 
  deriving Show


genPar :: Int -> [IO Point]
genPar num = map gen [1..num]

gen :: Int -> IO Point
gen _ = do 
    a <- getStdRandom (randomR (0, 1)) :: IO Float
    b <- getStdRandom (randomR (0, 1)) :: IO Float
    let p = Point a b
    return p
