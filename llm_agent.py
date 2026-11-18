import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from data_loader import load_json
from retriever import retrieve_top_docs

load_dotenv()


def search_company_docs(query: str) -> str:
    """Searches local documents and returns the best matching text."""
    docs = load_json("data/documents.json")
    matches = retrieve_top_docs(query, docs, top_k=1)
    if not matches:
        return "No relevant documents found."
    return f"[{matches[0]['topic']}]: {matches[0]['content']}"


TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_company_docs",
            "description": "Search internal documents to answer questions about Git, API keys, or LLM token budgets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search keywords to look up in the documents."
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def ask_agent(user_question: str, mock_mode: bool = False, max_steps: int = 3) -> str:
    """Sends a question to the LLM with multi-step tool-calling support."""
    if mock_mode:
        tool_result = search_company_docs(user_question)
        return f"[MOCK] Based on company documentation: {tool_result}"

    client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL")
    )
    model_name = os.getenv("LLM_MODEL")

    messages = [
        {
            "role": "system",
            "content": (
                "You are a concise, accurate assistant. Use search_company_docs once to find "
                "relevant internal documentation, then answer the user's question clearly in 2-3 sentences "
                "based strictly on the retrieved information."
            )
        },
        {"role": "user", "content": user_question}
    ]

    for _ in range(max_steps):
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            tools=TOOLS_SCHEMA
        )
        assistant_msg = response.choices[0].message

        # If the model finished and returned a normal text answer, return it!
        if not assistant_msg.tool_calls:
            return assistant_msg.content

        # Otherwise, execute all requested tool calls and continue the loop
        messages.append(assistant_msg)
        for tool_call in assistant_msg.tool_calls:
            if tool_call.function.name == "search_company_docs":
                args = json.loads(tool_call.function.arguments)
                print(f"[LLM CALLED TOOL] search_company_docs(query='{args['query']}')")
                result = search_company_docs(args["query"])

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

    return "Could not complete the answer within the maximum tool steps."


if __name__ == "__main__":
    question = "How should I protect my API key?"
    print(f"User: {question}\n")
    answer = ask_agent(question, mock_mode=False)
    print(f"\nFinal Answer:\n{answer}")