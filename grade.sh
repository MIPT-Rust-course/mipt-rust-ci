#!/usr/bin/env bash

echo "[INFO]   PROBLEM_NAME=\"$PROBLEM_NAME\""
echo "[INFO]   PROBLEM_SOLUTION=\"$PROBLEM_SOLUTION\""
echo "[INFO]   PROBLEM_ROOT=\"$PROBLEM_ROOT\""

./ci/scripts/file-routine.sh || exit 1
./ci/scripts/setup-deps.sh || exit 1
./ci/scripts/test-solution.sh || exit 1
./ci/scripts/submit-result.py || exit 1
