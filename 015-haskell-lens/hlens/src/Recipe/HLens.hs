{-# LANGUAGE MultiParamTypeClasses #-}
module Recipe.HLens where

import qualified Control.Lens
import           Control.Lens.Operators

-- Typeclasses

class Flippable a where
  flip :: a -> a

class Mergable a where
  merge :: a -> a -> a


-- Instances

instance Mergable