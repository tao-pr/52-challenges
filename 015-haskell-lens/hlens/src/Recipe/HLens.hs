{-# LANGUAGE MultiParamTypeClasses #-}
module Recipe.HLens where

import qualified Control.Lens
import           Control.Lens.Operators

class Flippable a where
  flip :: a -> a