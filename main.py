import os
from dotenv import load_dotenv
from data_loader import load_jsonl, save_jsonl
from llm_agent import ask_agent

# 1. Load environment configuration
load_dotenv()


def run_pipeline():
    # Verify API key exists before doing any work
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        raise ValueError("Missing LLM_API_KEY in .env file!")

    print(f"Configuration verified (Key starts with: {api_key[:8]}...)\n")

    # 2. Load input questions from JSONL
    input_path = "data/queries.jsonl"
    output_path = "data/final_answers.jsonl"
    queries = load_jsonl(input_path)
    print(f"Loaded {len(queries)} queries from {input_path}.\n")

    # 3. Process each query through the tool-calling LLM agent
    results = []
    for item in queries:
        q_id = item["query_id"]
        question = item["question"]
        print(f"--- Processing [{q_id}]: {question} ---")

        answer = ask_agent(question, mock_mode=False)
        print(f"Answer: {answer}\n")

        results.append({
            "query_id": q_id,
            "question": question,
            "answer": answer
        })

    # 4. Save all results to a new JSONL file
    save_jsonl(output_path, results)
    print(f"Done! Saved {len(results)} answers to {output_path}.")


if __name__ == "__main__":
    run_pipeline()