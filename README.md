# python-json-benchmarker
A benchmarking of reading JSON files with Python vs native code

## Benchmarks

### 27MB of JSON (2000000 items)
* Python: ~3.5s
* Python (using Rust library): ~1.2s
* Natively: ~1.0s
