{-# LANGUAGE MultiParamTypeClasses #-}
module Recipe.HLens where

import qualified Control.Lens
import           Control.Lens.Operators

-- Data

data Coord a = 
  Coord  { x :: a, y :: a } | NoWhere |
  ECoord { x :: a, y :: a, tlx :: a, tly :: a }  -- with tolerance of measurements


-- Typeclasses

class Vec a where
  i :: Ord b => a -> Maybe b
  j :: Ord b => a -> Maybe b