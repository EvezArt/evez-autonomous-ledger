#!/usr/bin/env bash
# Fail closed unless exactly the expected number of stage outcomes are present
# and every outcome explicitly reports success.
set -euo pipefail

outcomes_csv="${1-}"
expected_count="${2:-27}"

if [[ ! "$expected_count" =~ ^[1-9][0-9]*$ ]]; then
  echo "invalid expected stage count: $expected_count" >&2
  exit 2
fi

IFS=',' read -r -a outcomes <<< "$outcomes_csv"

if (( ${#outcomes[@]} != expected_count )); then
  echo "stage outcome count mismatch: expected=$expected_count observed=${#outcomes[@]}" >&2
  exit 1
fi

for index in "${!outcomes[@]}"; do
  outcome="${outcomes[$index]}"
  if [[ "$outcome" != "success" ]]; then
    echo "stage[$index] is not an explicit success (outcome='${outcome:-<empty>}'); refusing green result" >&2
    exit 1
  fi
done

echo "validated $expected_count explicit successful stage outcomes"
