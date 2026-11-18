import json

def load_json(filepath: str) -> list[dict]:
    """Reads a standard JSON file and returns its contents."""
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def load_jsonl(filepath: str) -> list[dict]:
    """Reads a JSONL file line by line and returns a list of dictionaries."""
    records = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            clean_line = line.strip()
            if clean_line: #Skip empty lines safely
                records.append(json.loads(clean_line))
    return records

def save_jsonl(filepath: str, records: list[dict]) -> None:
    """Writes a list of dictionaries to a JSONL file (one JSON per line)."""
    with open(filepath, "w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii =False) + "\n")


if __name__ == "__main__":
    # 1. Read JSON documents
    docs = load_json("data/documents.json")
    print(f"Loaded {len(docs)} documents from JSON.")

    #2. Read JSONL queries
    queries = load_jsonl("data/queries.jsonl")
    print(f"Loaded {len(queries)} queries from JSONL.")

    # 3. Create sample output and save to JSONL
    results = [
        {"query_id": q["query_id"], "status": "processed"} for q in queries
    ]
    save_jsonl("data/output.jsonl", results)
    print("Saved output to data/output.jsonl!")
      
