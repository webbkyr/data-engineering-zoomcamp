#!/bin/bash
set -euo pipefail

encoded_file=$(base64 -i .env.json)
echo "SECRET_GCP_KESTRA_AUTH=$encoded_file" > .env-encoded
