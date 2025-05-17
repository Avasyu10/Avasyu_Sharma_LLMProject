from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_TOKEN")
client = InferenceClient(
provider="sambanova", 
api_key=HUGGING_FACE_API_KEY,
)

def query_llm_with_context(query, context):

    try:
        prompt = f"Context: {context}\n\nQuestion: {query}"
        completion = client.chat.completions.create(
        model="Qwen/QwQ-32B", 
        messages=[
        {"role": "system", "content": "You are a helpful assistant. Use the provided context to answer the user's question."},
        {"role": "user", "content": prompt}
        ], max_tokens=500,
        )

        return completion.choices[0].message.content if completion.choices else "No response received."

    except Exception as e:
        return f"Error: {e}"