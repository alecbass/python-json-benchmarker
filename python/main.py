import json
import os
from io import open
from time import perf_counter
from typing import Any

import humanize
from json_benchmarker import read_json, generate_random_json, read_rust_chunked, Item


def item_from_dict(data: dict[str, Any]) -> Item:
    """
    Transforms a dictionaty of items into an Item.

    Args:
        data: The dictionary
    Raises:
        ValueError: If the dictionary is of invalid format, if the id field is not an integer
    """
    id = int(data.pop("id"))
    name = data.pop("name")
    description = data.pop("description")

    if any(item is None for item in [id, name, description]):
        raise ValueError("Received invalid item")

    return Item(id, name, description)


def write_with_python(path: str, count: int) -> str:
    """
    Generates a huge amount of JSON and writes it into a file.
    I did this so I didn't have to download and keep track of a massive file.

    Args:
        path: The file path to write to
        count: How many items to write
    Returns:
        The humanised file size
    """
    items: list[dict[str, str | int]] = []

    with open(path, "w") as file:
        for i in range(count):
            # Making an item here to mimic the Rust logic and ensure each parameter has correct typing
            item = Item(i, f"User {i}", f"A description for user {i}")
            items.append({"id": item.id, "name": item.name, "description": item.description})

        json.dump(items, file, separators=(",", ":"))

    file_size = os.path.getsize(path)
    return humanize.naturalsize(file_size)


def write_with_rust(path: str, count: int) -> str:
    """
    Writes a given amount of random JSON using the Rust binding.

    Args:
        path: The file path to write to
        count: How many items to write
    Returns:
        The humanised file size
    Raises:
        ValueError: If one of the JSON items couldn't be parsed as an Item
    """
    file_size = generate_random_json(path, count)
    return humanize.naturalsize(file_size)


def read_with_python(path: str) -> list[Item]:
    """
    Reads a given file and parses each JSON object as an Item.

    Args:
        path: The file path to read from
    Returns:
        A list of retrieved items
    Raises:
        ValueError: If one of the JSON items couldn't be parsed as an Item
    """
    items: list[Item] = []

    with open(path) as file:
        data = json.load(file)

        for item in data:
            items.append(item_from_dict(item))

    return items


def read_python_chunked(path: str, limit: int) -> list[Item]:
    """
    Butchered implementation of https://github.com/ICRAR/ijson/blob/master/src/ijson/backends/python.py
    """
    with open(path) as file:
        buffer = ""
        is_within_item = False

        items: list[Item] = []

        while True:
            char = file.read(1)

            if char == "":
                # End of file
                break

            if char == "{":
                is_within_item = True

            if not is_within_item:
                continue

            buffer += char

            if char == "}":
                is_within_item = False
                item_json = json.loads(buffer)
                item = item_from_dict(item_json)
                items.append(item)

                if len(items) == limit:
                    # TODO(alec): Yield items at this stage
                    items.clear()

                buffer = ""

    return []


def read_with_rust(path: str) -> list[Item]:
    """
    Reads a given file and parses each JSON object as an Item, using the Rust binding.

    Args:
        path: The file path to read from
    Returns:
        A list of retrieved items
    Raises:
        ValueError: If one of the JSON items couldn't be parsed as an Item
    """
    return read_json(path)


def main():
    file_path = "output.json"
    item_count_to_write = 20000

    start = perf_counter()
    file_size = write_with_rust(file_path, item_count_to_write)
    end = perf_counter()
    duration = end - start
    print(f"Rust wrote {file_size} to {file_path} after {duration}s")

    start = perf_counter()
    file_size = write_with_python(file_path, item_count_to_write)
    end = perf_counter()
    duration = end - start
    print(f"Python wrote {file_size} to {file_path} after {duration}s")

    start = perf_counter()
    items = read_with_rust(file_path)
    end = perf_counter()
    duration = end - start
    print(f"Rust read {len(items)} after {duration}s")

    start = perf_counter()
    items = read_with_python(file_path)
    end = perf_counter()
    duration = end - start
    print(f"Python read {len(items)} after {duration}s")

    start = perf_counter()
    items = read_rust_chunked(file_path, 20)
    end = perf_counter()
    duration = end - start
    print(f"Rust read {len(items)} after {duration}s (chunked)")

    start = perf_counter()
    items = read_python_chunked(file_path, 20)
    end = perf_counter()
    duration = end - start
    print(f"Python read {len(items)} after {duration}s (chunked)")


if __name__ == "__main__":
    main()
