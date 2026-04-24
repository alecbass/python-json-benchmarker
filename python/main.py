import json
import os
from time import perf_counter
from typing import Any

import humanize
from faker import Faker
from json_benchmarker import read_json, Item


def item_from_dict(data: dict[str, Any]) -> Item:
    """
    Transforms a dictionaty of items into an Item.

    Args:
        data: The dictionary
    Raises:
        ValueError: If the dictionary is of invalid format
    """
    name = data.pop("name")
    language = data.pop("language")
    id = data.pop("id")
    bio = data.pop("bio")
    version = data.pop("version")

    if any(item is None for item in [name, language, id, bio, version]):
        raise ValueError("Received invalid item")

    return Item(name, language, id, bio, version)


def generate_random_json(path: str, limit: int = 100) -> None:
    """
    Generates a huge amount of JSON and writes it into a file.

    I did this so I didn't have to download and keep track of a massive file.
    """
    faker = Faker()
    items: list[dict[str, str | float]] = []

    with open(path, "wb") as file:
        for i in range(limit):
            name = faker.first_name()
            language = faker.language_name()
            id = str(i)
            bio = faker.sentence(nb_words=10)  # , variable_nb_words=["Person", "Thing", "Language", "Item"])
            version = 1.0
            items.append({"name": name, "language": language, "id": id, "bio": bio, "version": version})

        json_bytes = json.dumps(items).encode("utf-8")
        file.write(json_bytes)

    file_size = os.path.getsize(path)
    file_size_readable = humanize.naturalsize(file_size)
    print(f"Written file is {file_size_readable}")


def read_with_rust(path: str) -> list[Item]:
    return read_json(path)


def read_with_python(path: str) -> list[Item]:
    items: list[Item] = []

    with open(path) as file:
        contents = file.read().replace("\n", "")
        data = json.loads(contents)

        for item in data:
            items.append(item_from_dict(item))

    return items


def main():
    file_path = "output.json"

    start_write = perf_counter()
    generate_random_json(file_path, limit=200000)
    end_write = perf_counter()
    duration_write = end_write - start_write
    print(f"File written to {file_path} after {duration_write}s")

    start_python = perf_counter()
    read_with_python(file_path)
    end_python = perf_counter()
    duration_python = end_python - start_python
    print(f"Python took {duration_python}s to run")

    start_rust = perf_counter()
    read_with_rust(file_path)
    end_rust = perf_counter()
    duration_rust = end_rust - start_rust
    print(f"Rust took {duration_rust}s to run")


if __name__ == "__main__":
    main()
