# python-json-benchmarker
A benchmarking of reading JSON files with Python vs native code

## Benchmarks

### 27MB of JSON (2000000 items)
* Python: ~3.5s
* Python (using Rust library): ~1.2s
* Natively: ~1.0s

# Bibliography
This feels like a school assignment lol

### Python compilation
[https://www.geeksforgeeks.org/python/internal-working-of-python/]()


# Talk flow (WIP)

1. Lore Introduction
2. Who am I
3. Programming background and interests
4. What this talk is (how to leverage native code in Python and if you should)
5. What this talk is not (a Rust-specific talk)
6. Background: Bidhive task reading large JSON files of contract data
7. Attempting it in Python: reading entire file, chunking with `ijson`
8. Side project in Rust: it was much faster
9. Why? Language comparison: writing machine code, compile-to-assembly, compile-to-bytecode, just-in-time compilation
10. Industries which use native code vs industries which use Python
11. A practical example: The world's worst JSON parser
12. My approach: act as the maintainer of a JSON parsing library which reads from a file
13. Two versions: Native Python, and Rust with bindings available through Maturin + Pyo3
14. Focusing on having near-identical business logic across the two versions
15. Python codebase overview: what it does, the ChunkedReader class
16. Rust codebase overview: similar logic, how Maturin turns it into a Python library. Show how the `.so` file is imported through `python -m site` and `python -c "import json_benchmarker; print(json_benchmarker.__spec__)"`
# TODO: Explain how the .whl file becomes importable
17. The results of reading a large file in the Python library vs Rust library (80s vs 3s)
18. Why the speed differences? Pre-optimised machine code vs creating it on the fly, garbage collection
19. Tradeoffs as a library maintainer:
20. - Typing: make it yourself, pyo3-stub-gen
21.   - Show how as a maintainer, static typing enforces the correct type vs type hints don't
22. - Platform-specific packages: native code needs to be compiled for each system, Python does not
23. - Now need to be across two languages
24. Why not use `ijson` and compare that? Because depending on how you use it, its core logic is written in C
25. Why doesn't everyone use native code?
26. - The dreaded "it depends"
27. - Most of the time, it isn't necessary
28. - In web development, most of your "delay" will be slow database queries and latency
29.   - 10ms vs 50ms for a function call doesn't matter if someone uploads a file over 3G
30. Thoughts? Concerns? Feelings? Hatred?
