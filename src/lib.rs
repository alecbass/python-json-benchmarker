mod chunked_reader;
mod data;
mod error;

use std::{
    fs::{File, metadata},
    io::{BufReader, BufWriter, Write},
};

use pyo3::{exceptions::PyValueError, prelude::*};
use pyo3_stub_gen::define_stub_info_gatherer;
use pyo3_stub_gen_derive::gen_stub_pyfunction;

use chunked_reader::ChunkedReader;
use data::Item;
use error::Error;

impl From<Error> for PyErr {
    fn from(e: Error) -> Self {
        PyValueError::new_err(format!("JSON benchmarker error: {e}"))
    }
}

pub fn read_json_native(path: &str) -> Result<Vec<Item>, Error> {
    let file = match File::open(path) {
        Ok(file) => file,
        Err(e) => return Err(Error::IoError(e)),
    };

    let reader = BufReader::new(file);
    let items: Result<Vec<Item>, serde_json::Error> = serde_json::from_reader(reader);

    if let Err(e) = items {
        eprintln!("Error parsing items: {e}");
        return Err(Error::JsonError(e));
    }

    Ok(items.unwrap())
}

#[gen_stub_pyfunction]
#[pyfunction]
pub fn read_json(path: &str) -> Result<Vec<Item>, Error> {
    let file = match File::open(path) {
        Ok(file) => file,
        Err(e) => return Err(Error::IoError(e)),
    };

    let reader = BufReader::new(file);
    let items: Result<Vec<Item>, serde_json::Error> = serde_json::from_reader(reader);

    if let Err(e) = items {
        eprintln!("Error parsing items: {e}");
        return Err(Error::JsonError(e));
    }

    Ok(items.unwrap())
}

#[gen_stub_pyfunction]
#[pyfunction]
pub fn create_chunked_reader(path: &str, limit: usize) -> Result<ChunkedReader, Error> {
    let file = match File::open(path) {
        Ok(file) => file,
        Err(e) => return Err(Error::IoError(e)),
    };

    Ok(ChunkedReader::new(file, limit))
}

#[gen_stub_pyfunction]
#[pyfunction]
pub fn generate_random_json(path: &str, count: i32) -> Result<u64, Error> {
    let file = match File::create(path) {
        Ok(file) => file,
        Err(e) => return Err(Error::IoError(e)),
    };

    let mut writer = BufWriter::new(file);
    let mut items = Vec::<Item>::with_capacity(count as usize);

    for i in 0..count {
        let item = Item::new(
            i,
            format!("User {i}"),
            format!("A description for user {i}"),
        );
        items.push(item);
    }

    if let Err(e) = serde_json::to_writer(&mut writer, &items) {
        return Err(Error::JsonError(e));
    }

    let file_details = match metadata(path) {
        Ok(details) => details,
        Err(e) => return Err(Error::IoError(e)),
    };

    Ok(file_details.len())
}

#[gen_stub_pyfunction]
#[pyfunction]
pub fn incremental_write(path: &str, count: i32) -> Result<(), Error> {
    let file = match File::create(path) {
        Ok(file) => file,
        Err(e) => return Err(Error::IoError(e)),
    };

    let mut writer = BufWriter::new(file);
    if let Err(e) = writer.write(&[b'[']) {
        return Err(Error::IoError(e));
    }

    for i in 0..count {
        let item = Item::new(
            i,
            format!("User {i}"),
            format!("A description for user {i}"),
        );

        if let Err(e) = serde_json::to_writer(&mut writer, &item) {
            return Err(Error::JsonError(e));
        }

        let is_last = i == count - 1;

        if !is_last {
            if let Err(e) = writer.write(&[b',']) {
                return Err(Error::IoError(e));
            }
        }
    }

    if let Err(e) = writer.write(&[b']']) {
        return Err(Error::IoError(e));
    }

    Ok(())
}

#[pymodule]
fn json_benchmarker(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_json, m)?)?;
    m.add_function(wrap_pyfunction!(generate_random_json, m)?)?;
    m.add_function(wrap_pyfunction!(create_chunked_reader, m)?)?;
    m.add_function(wrap_pyfunction!(incremental_write, m)?)?;

    m.add_class::<Item>()?;
    m.add_class::<ChunkedReader>()?;

    Ok(())
}

// Define a function to gather stub information.
define_stub_info_gatherer!(stub_info);
