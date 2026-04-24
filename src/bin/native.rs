use std::time;

use json_benchmarker::read_json_native;

fn main() -> Result<(), ()> {
    let now = time::Instant::now();
    let start = now.elapsed().as_millis();
    let items = read_json_native("output.json").unwrap();
    let after = now.elapsed().as_millis();
    let elapsed = (after as f64 - start as f64) / 1000.0;

    println!("Took this long natively: {}s", elapsed);

    Ok(())
}
