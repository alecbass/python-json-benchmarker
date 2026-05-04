use std::{
    fs::File,
    io::{BufReader, Read},
};

use pyo3::prelude::*;
use pyo3_stub_gen_derive::{gen_stub_pyclass, gen_stub_pymethods};

use super::data::Item;

#[gen_stub_pyclass]
#[pyclass]
pub struct ChunkedReader {
    reader: BufReader<File>,
    limit: usize,
}

impl ChunkedReader {
    // Create a new method, deliberately Rust-only so as to use the File struct
    pub fn new(file: std::fs::File, limit: usize) -> Self {
        let reader = BufReader::new(file);
        Self { reader, limit }
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl ChunkedReader {
    fn __next__(&mut self) -> Option<Vec<Item>> {
        self.next()
    }
}

impl Iterator for ChunkedReader {
    type Item = Vec<Item>;

    // Iterates through a few characters of the file to create a given number of Items from JSON
    // Returns None if no more items could be read
    fn next(&mut self) -> Option<Self::Item> {
        let mut buffer = Vec::<u8>::new();
        let mut items = Vec::<Item>::new();
        let mut is_within_item = false;

        loop {
            let mut char_buffer = [0; 1];
            let read_result = self.reader.read(&mut char_buffer);

            if let Err(_e) = read_result {
                // return Err(Error::IoError(e));
                return None;
            }

            let is_last = read_result.unwrap() == 0;

            if is_last {
                break;
            }

            let byte = char_buffer[0];
            let char = char::from(byte);

            if char == '{' {
                is_within_item = true;
            }

            if !is_within_item {
                continue;
            }

            buffer.push(byte);

            if char == '}' {
                is_within_item = false;
                let item_json = serde_json::from_slice(&buffer);

                if let Err(_e) = item_json {
                    // return Err(Error::JsonError(e));
                    return None;
                }

                let item: Item = item_json.unwrap();
                items.push(item);

                if items.len() == self.limit {
                    // TODO(alec): Yield items at this stage
                    return Some(items);
                }

                buffer.clear();
            }
        }

        None
    }
}
