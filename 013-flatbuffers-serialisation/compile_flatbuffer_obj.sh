#!/bin/bash

export FLATBUFFER_SRC_DIR=$HOME/3rd/flatbuffers

$FLATBUFFER_SRC_DIR/flatc --cpp -o headers/ schemas/data.schema