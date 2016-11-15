#!/bin/bash

shaddock -f shaddock/tests/model/image-tests.yml --debug -vvv build all
shaddock -f shaddock/tests/model/image-tests.yml --debug -vvv start all
shaddock -f shaddock/tests/model/image-tests.yml --debug -vvv remove all

shaddock -f shaddock/tests/model/host-tests.yml --debug -vvv build all
shaddock -f shaddock/tests/model/host-tests.yml --debug -vvv start all
shaddock -f shaddock/tests/model/host-tests.yml --debug -vvv remove all

shaddock -f shaddock/tests/model/scheduler-tests.yml --debug -vvv build all
shaddock -f shaddock/tests/model/scheduler-tests.yml --debug -vvv start all
shaddock -f shaddock/tests/model/scheduler-tests.yml --debug -vvv remove all

shaddock -f shaddock/tests/model/service-tests.yml --debug -vvv build all
shaddock -f shaddock/tests/model/service-tests.yml --debug -vvv start all
shaddock -f shaddock/tests/model/service-tests.yml --debug -vvv remove all

