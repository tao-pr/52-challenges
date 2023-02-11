{-# LANGUAGE OverloadedStrings #-}

module Main (main) where

import Lib
import Payload
import Data.Text (Text)
import Data.Text.Lazy (fromStrict)
import Control.Monad.IO.Class
import Web.Scotty -- Scotty is a web framework inspired by Ruby's Sinatra
import GHC.Base
import Debug.Trace

main :: IO ()
main = routes

routes :: IO () -- taotodo: add DB connection as 1st arg
routes = 
  scotty 3333 $ do
    -- validate if [[Payload]] is valid
    post "/validate" $ do
      payload <- jsonData
      traceM ("payload: " ++ show payload)
      valid <- liftIO . returnIO $ isValid payload
      json $ response valid

    -- extract payload containing gzipped of [[Unzipped]]
    post "/extract" $ do
      payload <- jsonData
      traceM ("payload: " ++ show payload)
      uz <- liftIO . returnIO $ unzipped payload
      json $ uz

    -- zip and return a utf8 bytestring of [[Unzipped]]
    post "/zip" $ do 
      uz <- jsonData -- for zip endpoint, data has to be "Unzipped" format
      traceM ("received: " ++ show uz)
      zz <- liftIO . returnIO $ zipMe uz
      traceM ("zipped: " ++ show zz)
      html $ fromStrict zz

    get "/" $ do
      html $ mconcat ["<bold>Hello, there!</bold>", "<p>", "this works!", "</p>"]

