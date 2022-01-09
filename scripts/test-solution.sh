#!/usr/bin/env bash

if [ -z "$CI" ];
then
    echo "Not in CI. Exiting"
    exit 1
fi

cd "$PROBLEM_ROOT"

cargo fmt -- --check || exit 1
cargo clippy -- -D warnings || exit 1
cargo test || exit 1

if [[ "$PROBLEM_NAME" =~ ^()$ ]];
then
    cargo criterion || exit 1
fi

echo "[INFO]   Testing returned no errors"
