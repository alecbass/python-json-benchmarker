use std::{fs::File, io::BufReader};

use pyo3::{exceptions::PyValueError, prelude::*};
use thiserror::Error;

use data::Item;

mod data;

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

// #[pyfunction]
// fn read_json(path: &str) -> PyResult<Vec<Item>> {
//     read_json_core(path).map_err(PyErr::new(None))
// }

/// A Python module implemented in Rust. The name of this function must match
/// the `lib.name` setting in the `Cargo.toml`, else Python will not be able to
/// import the module.
#[pymodule]
fn json_benchmarker(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(read_json, m)?)?;

    Ok(())
}
