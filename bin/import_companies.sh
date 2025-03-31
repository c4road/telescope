#!/bin/bash

API_ENDPOINT="http://localhost:8000/import_company_data/"

CSV_FILE="company-dataset.csv"

if [ ! -f "$CSV_FILE" ]; then
  echo "Error: CSV file '$CSV_FILE' not found."
  exit 1
fi

curl -X POST -F "file=@$CSV_FILE" "$API_ENDPOINT" | jq

echo "Company data import completed."
