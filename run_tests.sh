#!/bin/bash

shaddock -f tests/model/shaddock.yml rm            --debug   # --verbose   
shaddock -f tests/model/010-img-tests.yml build    --debug   # --verbose   
shaddock -f tests/model/shaddock.yml ps            --debug   # --verbose   
shaddock -f tests/model/shaddock.yml start         --debug   # --verbose   
shaddock -f tests/model/shaddock.yml rm            --debug   # --verbose   
