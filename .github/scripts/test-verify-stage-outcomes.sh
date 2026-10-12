#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFIER="$ROOT/verify-stage-outcomes.sh"
EXPECTED=27

make_csv() {
  local value="$1"
  local -a values=()
  local i
  for ((i = 0; i < EXPECTED; i++)); do values+=("$value"); done
  local IFS=,
  printf '%s' "${values[*]}"
}

expect_rc() {
  local label="$1" expected_rc="$2"
  shift 2
  local actual_rc=0
  "$@" >/dev/null 2>&1 || actual_rc=$?
  if [[ "$actual_rc" -ne "$expected_rc" ]]; then
    echo "FAIL: $label expected exit=$expected_rc got=$actual_rc" >&2
    exit 1
  fi
  echo "PASS: $label"
}

success_csv="$(make_csv success)"
expect_rc "all stages successful" 0 bash "$VERIFIER" "$success_csv" "$EXPECTED"

for rejected in failure cancelled skipped pending ""; do
  values=()
  for ((i = 0; i < EXPECTED; i++)); do values+=(success); done
  values[13]="$rejected"
  IFS=, csv="${values[*]}"
  expect_rc "reject outcome '${rejected:-empty}'" 1 bash "$VERIFIER" "$csv" "$EXPECTED"
done

expect_rc "reject missing stage outcomes" 1 bash "$VERIFIER" "success,success" "$EXPECTED"
expect_rc "reject invalid expected count" 2 bash "$VERIFIER" "$success_csv" "0"

echo "truth-gate helper regression tests: PASS"
