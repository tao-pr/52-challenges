{-# LANGUAGE MultiParamTypeClasses #-}

module MC where

import Sample (Sample())

class MC m where
  simulate :: m -> Int -> Float

-- Simulators with a tolerance parameter
data Simulator = PiMC | EulerMC
  
instance MC Simulator where
  simulate p n = error "" 