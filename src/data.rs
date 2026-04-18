use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
    name: String,
    language: String,
    id: String,
    bio: String,
    version: f32,
}
