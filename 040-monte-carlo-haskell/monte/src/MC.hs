{-# LANGUAGE MultiParamTypeClasses #-}

module MC where

import Sample (genPar, foldCount, Point(..))
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


-- simulate n rounds for Pi estimation
simulatePi :: Int -> IO Float
simulatePi n = do 
  samples <- parallel $ genPar n
  -- print samples
  let size = int2Float $ length samples
  let x = int2Float . snd $ foldCount inUCircle (0,0) samples
  printf "num in unit circle : %f\n" x
  returnIO $ 4 * x / size 

simulateEuler :: Int -> IO Float
simulateEuler n = returnIO 1.0 -- taotodo

inUCircle :: Point -> Bool
inUCircle (Point x y) = 1 >= sqrt (x**2 + y**2)

