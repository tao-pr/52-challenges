{-# LANGUAGE OverloadedStrings #-}

module Main (main) where

import Lib
import Payload
import Control.Monad.IO.Class
import Web.Scotty -- Scotty is a web framework inspired by Ruby's Sinatra
import GHC.Base

main :: IO ()
main = routes

routes :: IO () -- taotodo: add DB connection as 1st arg
routes = 
  scotty 3333 $ do
    post "/validate" $
      do
        -- parse request body
        payload <- jsonData
        isValid <- liftIO $ returnIO $ isValidPayload payload

        -- return
        json $ valid "payload is valid"

