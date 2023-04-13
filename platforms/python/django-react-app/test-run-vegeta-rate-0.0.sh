#!/usr/bin/env bash
set -euxo pipefail

export TARGET_BASE="http://127.0.0.1:8010"

. _test-run-vegeta-common.sh
