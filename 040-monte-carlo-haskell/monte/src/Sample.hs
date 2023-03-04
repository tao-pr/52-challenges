module Sample where

import System.Random(Random)

data (Random a, Floating a) => Sample a = S a a
