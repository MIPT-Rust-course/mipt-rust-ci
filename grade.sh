#!/usr/bin/env bash

echo "[INFO]   PROBLEM_NAME=\"$PROBLEM_NAME\""
echo "[INFO]   PROBLEM_SOLUTION=\"$PROBLEM_SOLUTION\""
echo "[INFO]   PROBLEM_ROOT=\"$PROBLEM_ROOT\""

./ci/scripts/file-routine.sh
./ci/scripts/setup-deps.sh
./ci/scripts/test-solution.sh
./ci/scripts/submit-result.py
