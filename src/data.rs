use pyo3::pyclass;
use serde::{Deserialize, Serialize};

#[pyclass]
#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
    name: String,
    language: String,
    id: String,
    bio: String,
    version: f32,
}
