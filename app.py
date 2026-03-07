import json
import os
import numpy as np

from flask import Flask, render_template, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types


# -----------------------------
# Load API Key
# -----------------------------

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

app = Flask(__name__)


# -----------------------------
# Chunk Documents
# -----------------------------

def chunk_document(text, chunk_size=300):

    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


# -----------------------------
# Generate Embeddings
# -----------------------------

def generate_embedding(text):

    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )

    return response.embeddings[0].values


# -----------------------------
# Load / Cache Embeddings
# -----------------------------

EMBED_FILE = "embeddings.json"

chunks = []
embeddings = []

if os.path.exists(EMBED_FILE):

    print("Loading cached embeddings...")

    data = json.load(open(EMBED_FILE))

    for item in data:
        chunks.append(item["chunk"])
        embeddings.append(item["embedding"])

else:

    print("Generating embeddings (first run)...")

    documents = json.load(open("docs.json"))

    cache_data = []

    for doc in documents:

        doc_chunks = chunk_document(doc["content"])

        for chunk in doc_chunks:

            emb = generate_embedding(chunk)

            chunks.append(chunk)
            embeddings.append(emb)

            cache_data.append({
                "chunk": chunk,
                "embedding": emb
            })

    json.dump(cache_data, open(EMBED_FILE, "w"))

    print("Embeddings saved!")


# -----------------------------
# Similarity Search
# -----------------------------

def find_similar_chunks(query_embedding):

    similarities = cosine_similarity(
        [query_embedding],
        embeddings
    )[0]

    top_indices = np.argsort(similarities)[-3:][::-1]

    return [chunks[i] for i in top_indices]


# -----------------------------
# LLM Response
# -----------------------------

def get_llm_response(context, question):

    prompt = f"""
You are a helpful assistant.

Use ONLY the provided context to answer the question.

Context:
{context}

Question:
{question}

If the answer is not present in the context say:
"I don't have enough information."
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.candidates[0].content.parts[0].text


# -----------------------------
# Routes
# -----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():

    try:

        data = request.json
        message = data.get("message")

        if not message:
            return jsonify({"error": "Message required"}), 400


        # Generate query embedding
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=message,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
        query_embedding = response.embeddings[0].values


        # Retrieve relevant chunks
        similar_chunks = find_similar_chunks(query_embedding)

        context = " ".join(similar_chunks)


        # Generate LLM answer
        reply = get_llm_response(context, message)


        return jsonify({
            "reply": reply,
            "retrievedChunks": len(similar_chunks)
        })

    except Exception as e:

        return jsonify({"error": str(e)}), 500


# -----------------------------
# Run Server
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)