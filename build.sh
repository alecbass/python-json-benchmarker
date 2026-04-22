#!/usr/bin/env bash

set -euo

uv run maturin develop --uv
cargo run --bin stub_gen
