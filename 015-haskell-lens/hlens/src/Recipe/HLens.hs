{-# LANGUAGE MultiParamTypeClasses #-}
module Recipe.HLens where

import qualified Control.Lens
import           Control.Lens.Operators

-- Data

data P a b = P a b | Q a | R [b]

-- Typeclasses

class Flippable a where
  flip :: a -> a

-- Instances