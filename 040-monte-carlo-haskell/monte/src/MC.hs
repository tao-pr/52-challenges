{-# LANGUAGE MultiParamTypeClasses #-}

module MC where

import Sample (genPar, foldSplit, Point(..))
import GHC.Base(returnIO)
import Control.Concurrent.ParallelIO.Global(parallel)
import GHC.Float
import Text.Printf

class MC m where
  simulate :: m -> Int -> IO Float 

-- Simulators with a tolerance parameter
data Simulator = PiMC | EulerMC deriving Show
  
instance MC Simulator where
  simulate p n = case p of 
    PiMC -> simulatePi n
    EulerMC -> simulateEuler n

{-
  Simulate n rounds of Pi estimation with MCMC
  
  area of circle / area of square = p*r^2 / 4r^2 = pi / 4

  then:
    pi  = 4 * area of circle / area of square
       ~= 4 * num points in circle / total num points
-}
simulatePi :: Int -> IO Float
simulatePi n = do 
  samples <- parallel $ genPar n
  print $ take 30 samples
  let size = int2Float $ length samples
  let (xin,xout) = foldSplit inUCircle ([],[]) samples
  let x = int2Float $ length xin
  printf "num in unit circle : %f\n" x
  printf "num all            : %f\n" size
  returnIO $ 4 * x / size 

simulateEuler :: Int -> IO Float
simulateEuler n = returnIO 1.0 -- taotodo

inUCircle :: Point -> Bool
inUCircle (Point x y) = 1 > sqrt (x**2 + y**2)


