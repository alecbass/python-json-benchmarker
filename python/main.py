import json
import os
from io import open
from time import perf_counter

import humanize
from json_benchmarker import read_json, generate_random_json, create_chunked_reader, incremental_write, Item

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


def incremental_write_python(path: str, count: int) -> None:
    with open(path, "w") as file:
        # Start the array
        file.write("[")

        for i in range(count):
            # Making an item here to mimic the Rust logic and ensure each parameter has correct typing
            item = Item(i, f"User {i}", f"A description for user {i}")
            item_dict = {"id": item.id, "name": item.name, "description": item.description}

            json.dump(item_dict, file)

            is_last = i == count - 1

            if not is_last:
                file.write(",")

        # End the array
        file.write("]")


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
    chunked_reader = create_chunked_reader(file_path, 20)

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

    start = perf_counter()
    incremental_write_python(file_path, 9999999)
    end = perf_counter()
    duration = end - start
    print(f"Python incremental write took {duration}s")

    start = perf_counter()
    incremental_write(file_path, 9999999)
    end = perf_counter()
    duration = end - start
    print(f"Rust incremental write took {duration}s")


if __name__ == "__main__":
    main()
