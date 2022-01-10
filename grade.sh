#!/usr/bin/env bash

echo "[INFO]   PROBLEM_NAME=\"$PROBLEM_NAME\""
echo "[INFO]   PROBLEM_SOLUTION=\"$PROBLEM_SOLUTION\""
echo "[INFO]   PROBLEM_ROOT=\"$PROBLEM_ROOT\""
echo "[INFO]   USER_LOGIN=\"$USER_LOGIN\""

./ci/scripts/file-routine.sh || exit 1
./ci/scripts/setup-deps.sh || exit 1
./ci/scripts/test-solution.sh || exit 1

pip install gspread oauth2client || exit 1
echo "$GSHEET_API_TOKEN" > ci/scripts/token.json || exit 1
./ci/scripts/submit-result.py || exit 1
