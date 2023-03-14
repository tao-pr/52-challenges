module Sample where

import Control.Parallel.Strategies
import GHC.Base(returnIO)

data Point = Point Float Float 
  deriving Show

genPar :: Int -> [IO Point]
genPar num = [] -- taotodo

gen :: IO Point
gen = returnIO $ Point 0 0 -- taotodo

