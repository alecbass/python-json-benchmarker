use std::fmt::Display;

use pyo3::{pyclass, pymethods};
use pyo3_stub_gen_derive::gen_stub_pyclass;
use serde::{Deserialize, Serialize};

#[gen_stub_pyclass]
#[pyclass(get_all, frozen, str)]
#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
    name: String,
    language: String,
    id: String,
    bio: String,
    version: f32,
}

impl Display for Item {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.name)
    }
}

#[pymethods]
impl Item {
    #[new]
    pub fn new(name: String, language: String, id: String, bio: String, version: f32) -> Self {
        Self {
            name,
            language,
            id,
            bio,
            version,
        }
    }

    pub fn get_name(&self) -> &str {
        &self.name
    }
}
