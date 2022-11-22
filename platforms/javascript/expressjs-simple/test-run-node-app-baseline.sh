#!/usr/bin/env bash

export TARGET_BASE="http://127.0.0.1:3000"
echo '{"labels":[{"name":"baseTest", "value":"true"},{"name":"displayName", "value":"Base"}]}' > /tmp/custom-data.json

. _test-run-common.sh
