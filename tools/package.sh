#!/usr/bin/env bash
# Rebuild dist/trend-predictor.zip (the upload for Claude apps) from skills/trend-predictor.
set -euo pipefail
cd "$(dirname "$0")/../skills"
mkdir -p ../dist && rm -f ../dist/trend-predictor.zip
zip -rq ../dist/trend-predictor.zip trend-predictor -x '*/__pycache__/*' '*.pyc'
echo "wrote dist/trend-predictor.zip"
