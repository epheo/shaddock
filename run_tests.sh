#!/bin/bash

shaddock -f tests/model/010-img-tests.yml build all

for test_scenario in 010-img-tests.yml \
                     130-volume-tests.yml \
                     120-cmd-tests.yml \
                     200-hosts-tests.yml \
                     300-network-tests.yml \
                     400-jinja-tests.yml \
                     500-scheduler-tests.yml
do
  echo ""
  echo "# Running test scenario $test_scenario"
  echo "# ------------------------------------"
  # $1=--debug
  # $2=-vvv"
  shaddock -f tests/model/$test_scenario $1 $2 rm all > /dev/null
  shaddock -f tests/model/$test_scenario $1 $2 start all
  shaddock -f tests/model/$test_scenario $1 $2 rm all > /dev/null
  # shaddock -f tests/model/$test_scenario $opts logs all |tail -n600
done
