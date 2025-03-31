#!/bin/bash

API_ENDPOINT="http://localhost:8000/process_company/"

RULES_FILE="bin/rules.json"

if [ ! -f "$RULES_FILE" ]; then
  echo "Error: JSON file '$RULES_FILE' not found."
  exit 1
fi

curl -X POST \
  -H "Content-Type: application/json" \
  -d "@$RULES_FILE" \
  "$API_ENDPOINT" | jq

echo "Company data processing completed."
