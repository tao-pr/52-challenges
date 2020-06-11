{-# LANGUAGE MultiParamTypeClasses #-}  -- For multiple-typed classes
{-# LANGUAGE GADTs #-}                  -- For type-constraint typeclasses
{-# LANGUAGE TemplateHaskell #-}        -- For Prism & Lens

module Recipe.HLens where

import Control.Lens
import Control.Lens.TH 

-- Data

data Coord a = Coord { _x :: a, _y :: a } deriving (Eq, Ord, Show)
makeLenses ''Coord

data Coord3D a = Coord3D { _xx :: a, _yy :: a, _zz :: a } deriving (Eq, Ord, Show)
makeLenses ''Coord3D

data Where a = AtCoord (Coord a) | AtCoord3D (Coord3D a) | NW
  deriving (Eq, Ord, Show)
makePrisms ''Where

-- Oprs

getx :: Where a -> a
getx = error "Not supported"
  & outside _AtCoord .~ view x
  & outside _AtCoord3D .~ view xx

dist :: Coord a -> Coord a -> a
dist p q = error "not implemented"


