{-# LANGUAGE DeriveGeneric #-}

module Payload (Payload, Unzipped, isValidPayload, unzipped, valid) where

import Data.IORef
import Data.Text (Text)
import Data.ByteString.UTF8 (ByteString)
import Data.Aeson
import GHC.Generics

-- Raw request payload (with zipped data)
data Payload = Payload 
  { sessionId :: Text,
    zipped :: Text -- bytestring
  }
  deriving (Generic, Show)

-- Unzipped data in the payload
data Unzipped = Null | Unzipped
  { token :: Text,
    date :: Text,
    amount :: Int
  }

data Response = Response
  { isError :: Bool,
    msg :: Text
  }
  deriving (Generic, Show)


instance FromJSON Payload
instance ToJSON Response


isValidPayload :: Payload -> Bool
isValidPayload p = error "not implemented"

unzipped :: Payload -> Unzipped
unzipped p = error "not implemented"

valid :: Text -> Response 
valid t = Response True t