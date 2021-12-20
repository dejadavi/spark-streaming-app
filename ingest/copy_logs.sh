#!/bin/bash

set -euf -o pipefail;

DW_DATE=$(date '+%Y-%m-%d')
FILE_NAME="nvdcve-1.1-modified.json.gz"
FILE_PATH="https://nvd.nist.gov/feeds/json/cve/1.1/${FILE_NAME}"
BASE_PATH="dw_date=${DW_DATE}"
LOG_PATH="${BASE_PATH}/${FILE_NAME}"

echo "Attempting to download log $FILE_PATH"

mkdir -p "/local/logs/${BASE_PATH}"
wget  -O "/local/logs/${BASE_PATH}/${FILE_NAME}" $FILE_PATH

echo "File sucessfully copied."

ls "/local/logs/${BASE_PATH}"