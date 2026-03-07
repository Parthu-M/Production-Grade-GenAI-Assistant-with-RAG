# GenAI RAG Chat Assistant 🤖

An AI-powered chatbot built using **Retrieval-Augmented Generation (RAG)** and the **Google Gemini API**.
This application retrieves relevant information from a knowledge base using **semantic search and embeddings** and then generates accurate responses using a large language model.

---

## 🚀 Features

* AI-powered question answering
* Retrieval-Augmented Generation (RAG)
* Semantic search using embeddings
* Knowledge base stored in JSON documents
* Fast similarity search using cosine similarity
* Interactive chat interface
* Flask backend with HTML, CSS, and JavaScript frontend
* Environment variable support for API keys

---

## 🧠 How It Works

The system follows a **RAG pipeline**:

1. User submits a question through the web interface.
2. The question is converted into an **embedding vector**.
3. The system compares it with stored document embeddings using **cosine similarity**.
4. The most relevant chunks are retrieved.
5. The retrieved context is sent to the **Gemini LLM**.
6. The model generates a context-aware answer.

---

## 🏗 Project Structure

```
genai-chat-assistant/
│
├── app.py                # Flask backend
├── docs.json             # Knowledge base documents
├── embeddings.json       # Cached document embeddings
├── requirements.txt      # Python dependencies
│
├── static/
│   ├── script.js         # Frontend logic
│   └── styles.css        # UI styling
│
├── templates/
│   └── index.html        # Chat interface
│
└── .env                  # API key (not uploaded to GitHub)
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/yourusername/genai-chat-assistant.git
cd genai-chat-assistant
```

---

### 2️⃣ Create a virtual environment

```
python -m venv .venv
```

Activate it:

**Windows**

```
.venv\Scripts\activate
```

**Mac/Linux**

```
source .venv/bin/activate
```

---

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Add API Key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

You can get an API key from:

https://aistudio.google.com/app/apikey

---

### 5️⃣ Run the application

```
python app.py
```

Open your browser and go to:

```
http://localhost:5000
```

---

## 🌐 Deployment

This project can be deployed for free using:

* Render
* Railway
* Fly.io

Recommended: **Render**

Steps:

1. Push the project to GitHub
2. Connect the repo to Render
3. Set environment variable `GOOGLE_API_KEY`
4. Deploy the web service

---

## 🛠 Technologies Used

* Python
* Flask
* Google Gemini API
* Vector Embeddings
* Cosine Similarity Search
* HTML
* CSS
* JavaScript

---

## 📌 Example Use Cases

* AI customer support assistants
* Knowledge base search
* FAQ automation
* Internal company documentation search
* Helpdesk AI tools

---

## ⚠️ Notes

* The Gemini free tier has **API rate limits**.
* Embeddings are cached locally to reduce API usage.
* Do not upload `.env` to GitHub.

---

## 📄 License

This project is open source and available under the MIT License.
