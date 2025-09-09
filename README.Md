Ocean Bank RAG Chatbot
A conversational AI chatbot for a fictional "Ocean Bank," built using Python, FastAPI, and Google's Gemini Pro. The application leverages the Retrieval-Augmented Generation (RAG) pattern to answer user questions based on a local knowledge base of banking documents.

✨ Features
Conversational AI: Powered by Google's gemini-1.5-flash model for natural and helpful responses.

Retrieval-Augmented Generation (RAG): Provides context-aware answers by retrieving relevant information from a vector database before generating a response.

Real-time Streaming: Uses Server-Sent Events (SSE) to stream the AI's response token-by-token, creating a smooth "typing" effect.

Vector Search: Utilizes ChromaDB as a local vector store for efficient similarity searches.

Intent-Driven Prompts: Dynamically adjusts the AI's system prompt based on the detected intent of the user's question (e.g., loans, security, accounts).

Simple Web Interface: A clean and responsive frontend built with vanilla HTML, CSS, and JavaScript.

🏗️ Architecture (RAG Flow)
The application follows a standard Retrieval-Augmented Generation pattern:

User Query: The user asks a question through the web interface (e.g., "What are your savings account interest rates?").

API Request: The frontend sends the question to the FastAPI backend.

Retrieval: The backend embeds the user's question into a vector and queries ChromaDB to find the most relevant document chunks from its knowledge base.

Augmentation: The retrieved documents (context) are combined with the original question into a detailed prompt.

Generation: This augmented prompt is sent to the Gemini API. The model uses the provided context to generate an accurate and relevant answer.

Streaming Response: The generated answer is streamed back to the frontend and displayed to the user in real-time.

+----------------+      +------------------+      +----------------+      +---------------------+      +----------------+
|   User Input   |----->|  FastAPI Backend |----->|    ChromaDB    |----->|   Google Gemini API |----->|   User Interface|
| (via Frontend) |      | (main.py)        |      | (Vector Store) |      | (LLM Generation)    |      | (Streaming Text)|
+----------------+      +------------------+      +----------------+      +---------------------+      +----------------+

🛠️ Tech Stack
Backend: Python, FastAPI

AI & Vector Store: Google Generative AI (Gemini), ChromaDB, Sentence-Transformers

Frontend: HTML, CSS, JavaScript

Server: Uvicorn

🚀 Getting Started
Follow these instructions to set up and run the project locally.

Prerequisites
Python 3.9 or higher

An active Google AI Studio API Key. You can get one here.

1. Clone the Repository
git clone [https://github.com/your-username/ocean-bank-chatbot.git](https://github.com/your-username/ocean-bank-chatbot.git)
cd ocean-bank-chatbot

2. Install Dependencies
Install all the required Python packages using pip.

pip install -r requirements.txt

3. Set Up Environment Variables
Create a file named .env in the root of the project directory. This file will store your secret API key.

GEMINI_API_KEY="YOUR_GOOGLE_API_KEY_HERE"

Important: Never commit your .env file to version control.

4. Create the Vector Database
Run the chroma_setup.py script to embed the sample banking documents and populate the ChromaDB vector store. This only needs to be done once.

python chroma_setup.py

This will create a chroma_db directory in your project containing the vector data.

5. Run the Application
Start the FastAPI server using Uvicorn. The --reload flag enables hot-reloading for development.

uvicorn main:app --reload

6. Access the Chatbot
Once the server is running, open your web browser and navigate to:

http://127.0.0.1:8000

You should now be able to interact with the Ocean Bank chatbot!

📂 Project Structure
.
├── chroma_db/              # Directory for the persistent vector store (auto-generated)
├── .env                    # Your environment file for API keys (you create this)
├── chroma_setup.py         # Script to initialize and populate ChromaDB
├── index.html              # Frontend main page
├── main.py                 # FastAPI application server and API endpoints
├── prompt_templates.py     # Defines system prompts for different user intents
├── rag_service.py          # Core logic for the RAG pipeline
├── requirements.txt        # Python dependencies
├── script.js               # Frontend JavaScript for interactivity
├── styles.css              # Frontend CSS for styling
└── test_api.py             # Script for testing ChromaDB queries directly

LICENSE
This project is licensed under the MIT License. See the LICENSE file for details.