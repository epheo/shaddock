#!/bin/bash

shaddock -f tests/model/shaddock.yml rm
shaddock -f tests/model/010-img-tests.yml build
shaddock -f tests/model/shaddock.yml ps
shaddock -f tests/model/shaddock.yml start
shaddock -f tests/model/shaddock.yml rm
