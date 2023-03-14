{-# LANGUAGE MultiParamTypeClasses #-}

module MC where

import Sample (genPar)
import GHC.Base(returnIO)
import Control.Concurrent.ParallelIO.Global(parallel)

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
  returnIO 1.0 -- taotodo

simulateEuler :: Int -> IO Float
simulateEuler n = returnIO 1.0 -- taotodo