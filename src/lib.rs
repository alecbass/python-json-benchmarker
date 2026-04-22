mod data;

use std::{fs::File, io::BufReader};

use pyo3::{exceptions::PyValueError, prelude::*};
use pyo3_stub_gen::define_stub_info_gatherer;
use pyo3_stub_gen_derive::gen_stub_pyfunction;
use thiserror::Error;

use data::Item;

#[derive(Error, Debug)]
pub enum ReadError {
    #[error("Failed to read file")]
    IoError(#[from] std::io::Error),

    #[error("Error parsing JSON")]
    JsonError(#[from] serde_json::Error),
}

impl From<ReadError> for PyErr {
    fn from(e: ReadError) -> Self {
        PyValueError::new_err(format!("JSON benchmarker error: {e}"))
    }
}

#[gen_stub_pyfunction]
#[pyfunction]
fn read_json(path: &str) -> Result<Vec<Item>, ReadError> {
    let file = match File::open(path) {
        Ok(file) => file,
        Err(e) => return Err(ReadError::IoError(e)),
    };

    let reader = BufReader::new(file);
    let items: Result<Vec<Item>, serde_json::Error> = serde_json::from_reader(reader);

    if let Err(e) = items {
        eprintln!("Error parsing items: {e}");
        return Err(ReadError::JsonError(e));
    }

    Ok(items.unwrap())
}

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn json_benchmarker(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_json, m)?)?;
    m.add_class::<Item>()?;

    Ok(())
}

// Define a function to gather stub information.
define_stub_info_gatherer!(stub_info);
