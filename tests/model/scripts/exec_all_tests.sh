#!/bin/bash

shaddock -f tests/model/image-tests.yml --debug -vvv build all
shaddock -f tests/model/image-tests.yml --debug -vvv start all
shaddock -f tests/model/image-tests.yml --debug -vvv remove all

shaddock -f tests/model/host-tests.yml --debug -vvv build all
shaddock -f tests/model/host-tests.yml --debug -vvv start all
shaddock -f tests/model/host-tests.yml --debug -vvv remove all

shaddock -f tests/model/service-tests.yml --debug -vvv build all
shaddock -f tests/model/service-tests.yml --debug -vvv start all
shaddock -f tests/model/service-tests.yml --debug -vvv remove all

shaddock -f tests/model/scheduler-tests.yml --debug -vvv build all
shaddock -f tests/model/scheduler-tests.yml --debug -vvv start all
shaddock -f tests/model/scheduler-tests.yml --debug -vvv remove all
