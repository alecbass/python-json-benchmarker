#!/usr/bin/env bash

set -euo pipefail

uv run maturin develop --uv
cargo run --bin stub_gen
