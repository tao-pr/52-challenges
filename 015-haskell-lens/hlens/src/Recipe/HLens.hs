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

-- Instances


-- Oprs

getx :: Monoid a => Where a -> a
getx = mempty    -- Fallback case (non exhaustive)
  & outside _AtCoord .~ view x
  & outside _AtCoord3D .~ view xx

gety :: Monoid a => Where a -> a
gety = mempty
  & outside _AtCoord .~ view y
  & outside _AtCoord3D .~ view yy

getz :: Monoid a => Where a -> a
getz = mempty & outside _AtCoord3D .~ view zz

dist :: (Num a, Monoid a) => Where a -> Where a -> a
dist p q = 
  let { x' = (getx p) - (getx q)
      ; y' = (gety p) - (gety q)
      ; z' = (getz p) - (getz q) }
    in x'*x' + y'*y' + z'*z'


