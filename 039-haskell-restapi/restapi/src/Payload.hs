{-# LANGUAGE DeriveGeneric #-}
{-# LANGUAGE OverloadedStrings #-}

module Payload (Payload, response, Unzipped, isValid, unzipped, zipMe) where

import Prelude hiding(null)
import Data.IORef
import Data.Text (Text, null, pack, unpack, splitOn)
import Data.Text.Encoding
import Data.Char (ord, chr)
import Data.Aeson
import Data.ByteString.Lazy (fromStrict, toStrict, ByteString)
import Data.ByteString.Lazy.Internal (unpackChars, packChars)
import Codec.Compression.GZip(decompress, compress)
import GHC.Generics
import Debug.Trace

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
  deriving (Generic, Show)

data Response = Response
  { isError :: Bool,
    msg :: Text
  }
  deriving (Generic, Show)


-- serialisables
instance FromJSON Payload
instance ToJSON Response
instance ToJSON Unzipped
instance FromJSON Unzipped


isValid :: Payload -> Bool
isValid p = not . null $ sessionId p

response :: Bool -> Response
response v = if v 
  then Response False "valid request"
  else Response True "invalid request"

-- decode digit from text
t2c :: Text -> Char
t2c t = chr (read (unpack t) :: Int)

-- decode \x31\x139\x8\  ... into ByteString
-- needs to do 'tail' since it splits into [,31,139,8,..]
decodex :: Text -> ByteString
decodex s = packChars . (map t2c) . tail $ splitOn "\\x" s

unzipped :: Payload -> Maybe Unzipped
unzipped p = 
  -- needs `fromStrict` to convert ByteString -> Lazy.ByteString
  let z = decompress . decodex . zipped $ p
    in decode z :: Maybe Unzipped

pref :: String -> String
pref a = "\\x" ++ a

zipMe :: Unzipped -> Text
zipMe uz = 
  let bytes = unpackChars . compress . encode $ uz
    in pack $ concat $ map (pref . show . ord) $ bytes
  


