#!/usr/bin/env bash
set -euxo pipefail

export VE2IN_TOKEN="${INFLUX_TOKEN}"
export VE2IN_URL="${INFLUX_URL}"
export VE2IN_ORG="${INFLUX_ORG}"
export VE2IN_BUCKET="${INFLUX_BUCKET}"

INPUT_REQUESTS_FILE="vegeta-requests.txt"
RESULTS_FILE="results.json"

# Process the requests file
envsubst '${TARGET_BASE}' <"${INPUT_REQUESTS_FILE}" >input-requests.tmp.txt
mv input-requests.tmp.txt "${INPUT_REQUESTS_FILE}"

set +x
echo -e '\n ### START: Vegeta attack file'
cat "${INPUT_REQUESTS_FILE}"
echo -e '\n ### END'
set -x

# Wait until the endpoint is live
MAX_WAIT_SECONDS="60"
while [[ "$(curl --max-time 5 -s -o /dev/null -w ''%{http_code}'' ${TARGET_BASE})" != "200" ]]; do
    retries=$((${retries:-0}+1))
    if (( retries > MAX_WAIT_SECONDS )); then
        echo 'Too many retries, exiting.'
        exit 1
    fi
    echo "[$(date)] Waiting for the endpoint..."
    sleep 1;
done

# Run the attack
vegeta attack -targets "${INPUT_REQUESTS_FILE}" -rate=80 -duration=120s | vegeta encode > "${RESULTS_FILE}"

# Export the data to InfluxDB
vegeta2influx --input="${RESULTS_FILE}" --measurement=vegeta_request --tags pod_name="${POD_NAME}"

# Show the report
vegeta report "${RESULTS_FILE}"

# Wait for everything to be flushed
sleep 5
