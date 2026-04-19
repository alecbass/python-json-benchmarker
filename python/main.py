
def main():
    import json_benchmarker

    items = json_benchmarker.read_json("5MB.json")
    for item in items:
        print(item.get_name)

    print("Hello from python-json-benchmarker!")


if __name__ == "__main__":
    main()
