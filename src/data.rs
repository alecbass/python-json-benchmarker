use pyo3::pyclass;
use serde::{Deserialize, Serialize};

#[pyclass(get_all, set_all)]
#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
    name: String,
    language: String,
    id: String,
    bio: String,
    version: f32,
}
