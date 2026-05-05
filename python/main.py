import json
import os
from io import open
from time import perf_counter

import humanize
from json_benchmarker import read_json, generate_random_json, read_rust_chunked, read_rust_chunked_using_class, Item

from chunked_reader import PythonChunkedReader
from utils import item_from_dict


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

    Args:
        path: The file path to read from
        limit: How many items to oad for each chunk
    Returns:
        A list of retrieved items
    Raises:
        ValueError: If a JSON item is incorrect
    """
    all_items: list[Item] = []

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
                    all_items.extend(items)
                    items.clear()

                buffer = ""

    return items


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

    start = perf_counter()
    chunked_reader = read_rust_chunked_using_class(file_path, 20)

    while True:
        try:
            items = next(chunked_reader)
            # for item in items:
            #     print(item)
        except StopIteration:
            print("Reached the end")
            break

    end = perf_counter()
    duration = end - start
    print(f"Rust chunked read using class took {duration}s")

    start = perf_counter()
    python_chunked_reader = PythonChunkedReader.create(file_path, 20)
    while True:
        try:
            items = next(python_chunked_reader)
            # for item in items:
            #     print(item)
        except StopIteration:
            print("Reached the end")
            break
    end = perf_counter()
    duration = end - start
    print(f"Python chunked read using class took {duration}s")


if __name__ == "__main__":
    main()
