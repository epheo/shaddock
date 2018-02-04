#!/bin/bash

shdk -f tests/model/shaddock.yml rm            --debug   # --verbose   
shdk -f tests/model/010-img-tests.yml build    --debug   # --verbose   
shdk -f tests/model/shaddock.yml ps            --debug   # --verbose   
shdk -f tests/model/shaddock.yml start         --debug   # --verbose   
shdk -f tests/model/shaddock.yml rm            --debug   # --verbose   
shdk -f tests/model/600-load-tests.yaml ps            --debug   # --verbose   
