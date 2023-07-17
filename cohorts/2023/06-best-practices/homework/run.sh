#!/usr/bin/env bash

export AWS_ENDPOINT_URL="http://localhost:4566"

export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

python batch.py 2022 1