use std::{fs::File, io::BufReader};

use data::Item;

mod data;

fn read_json(path: &str) -> Result<Vec<Item>, ()> {
    let Ok(file) = File::open(path) else {
        return Err(());
    };
    let reader = BufReader::new(file);

    let items: Result<Vec<Item>, serde_json::Error> = serde_json::from_reader(reader);

    if let Err(e) = items {
        eprintln!("Error parsing items: {e}");
        return Err(());
    }

    Ok(items.unwrap())
}

fn main() -> Result<(), ()> {
    let items = read_json("5MB.json")?;
    println!("{items:?}");

    Ok(())
}
