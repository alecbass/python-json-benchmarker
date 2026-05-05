#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("Failed to read or write file")]
    IoError(#[from] std::io::Error),

    #[error("Error parsing JSON")]
    JsonError(#[from] serde_json::Error),
}
