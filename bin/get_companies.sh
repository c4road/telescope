#!/bin/bash

API_ENDPOINT="http://localhost:8000/get_companies/"

curl "$API_ENDPOINT" | jq

echo "Company data retrieval completed."
