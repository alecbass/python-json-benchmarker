use std::fmt::Display;

use pyo3::{pyclass, pymethods};
use pyo3_stub_gen_derive::{gen_stub_pyclass, gen_stub_pymethods};
use serde::{Deserialize, Serialize};

#[gen_stub_pyclass]
#[pyclass(get_all, frozen, str)]
#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
    id: i32,
    name: String,
    description: String,
}

impl Display for Item {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.name)
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl Item {
    #[new]
    pub fn new(id: i32, name: String, description: String) -> Self {
        Self {
            id,
            name,
            description,
        }
    }
}
