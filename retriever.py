import re
from data_loader import load_json

# Common filler words that don't help distinguish document topics
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "in", "on", "at",
    "to", "for", "with", "how", "what", "why", "do", "i", "my", "should"
}

def tokenize(text: str) -> set[str]:
    """Converts text to lowercase words and removes punctuation & stopwords."""
    words = re.findall(r"\b[a-z0-9]+\b", text.lower())
    return {w for w in words if w not in STOPWORDS}

def retrieve_top_docs(
        query: str, documents: list[dict], top_k: int = 1
) -> list[dict]:
    """Finds the top_k most relevant documents based on keyword overlap."""
    query_words = tokenize(query)
    scored_docs = []

    for doc in documents:
        # Combine topic  and content so both are searchable
        full_text = f"{doc['topic']} {doc['content']}"
        doc_words = tokenize(full_text)

        # Count how many unique query words appear in this documnet
        overlap = len(query_words.intersection(doc_words))
        scored_docs.append((overlap, doc))

    # Sort from highest overlap score to lowest
    scored_docs.sort(key=lambda item: item[0], reverse=True)

    # Return only the top_k documents that have at least 1 matching word
    return [doc for score, doc in scored_docs[:top_k] if score > 0]

if __name__ == "__main__":
    docs = load_json("data/documents.json")
    test_question = "How do I submit my final work?"

    matches = retrieve_top_docs(test_question, docs, top_k=1)

    print(f"Question: {test_question}\n")
    for match in matches:
        print(f"Matched [{match['id']} - {match['topic']}]: {match['content']}")