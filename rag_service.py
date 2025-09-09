import os
import logging
import re
from typing import AsyncGenerator
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import google.generativeai as genai
from prompt_templates import get_intent_prompt, detect_intent
import asyncio
from dotenv import load_dotenv

# --- Load environment variables from .env file ---
load_dotenv()

# --- Configuration ---
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GENERATIVE_MODEL_NAME = "gemini-1.5-flash"
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "banking_docs"

class RAGService:
    def __init__(self):
        """Initializes the RAG Service."""
        self._configure_logging()

        # Configure Gemini API
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logging.warning("⚠️ GEMINI_API_KEY environment variable not set. Using mock responses.")
            self.model = None
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(GENERATIVE_MODEL_NAME)
            logging.info("✅ Gemini API initialized successfully.")

        # Initialize Embedding Function
        self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )

        # Initialize ChromaDB Client
        settings = Settings(anonymized_telemetry=False)
        self.client = chromadb.PersistentClient(path=CHROMA_DB_PATH, settings=settings)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME, embedding_function=self.ef
        )
        logging.info("RAGService initialized successfully.")

    def _configure_logging(self):
        logging.getLogger("chromadb").setLevel(logging.CRITICAL)
        logging.getLogger("onnxruntime").setLevel(logging.CRITICAL)

    def _get_context(self, question: str, n_results: int = 3) -> str:
        results = self.collection.query(query_texts=[question], n_results=n_results)
        docs = results.get("documents", [[]])[0]
        return "\n\n".join(docs)

    def _construct_prompt(self, question: str, context: str) -> str:
        intent = detect_intent(question)
        system_prompt = get_intent_prompt(intent)
        
        prompt = f"""{system_prompt}

Here is some context that might be relevant to the user's question. Use it to provide a detailed and accurate answer. If the context is not relevant, rely on your general knowledge but always maintain the persona of an Ocean Bank assistant.

**Context:**
---
{context}
---

**User Question:** {question}

**Answer:**
"""
        return prompt

    async def get_answer(self, question: str) -> str:
        try:
            if self.model is None:
                mock_response = (
                    "Hello! I'm your Ocean Bank assistant. How can I help you today? "
                    "I can assist you with account information, loans, and general banking questions."
                )
                return " ".join(mock_response.split())
            
            context = self._get_context(question)
            prompt = self._construct_prompt(question, context)
            response = await self.model.generate_content_async(prompt)

            fixed_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', response.text.strip())
            fixed_text = re.sub(r'([.!?,])([A-Za-z])', r'\1 \2', fixed_text)
            return " ".join(fixed_text.split())
        except Exception as e:
            logging.error(f"Error in get_answer: {e}")
            return f"Sorry, I encountered an error: {e}."

    async def stream_answer(self, question: str) -> AsyncGenerator[str, None]:
        """Stream tokens as natural text chunks."""
        try:
            if self.model is None:
                mock_response = (
                    "Hello! I'm your Ocean Bank assistant. How can I help you today? "
                    "I can assist you with account information, loans, and general banking questions."
                )
                for word in mock_response.split():
                    yield word + " "
                    await asyncio.sleep(0.05)
                return

            context = self._get_context(question)
            prompt = self._construct_prompt(question, context)
            response_stream = await self.model.generate_content_async(prompt, stream=True)

            async for chunk in response_stream:
                if chunk.text:
                    fixed_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', chunk.text)
                    fixed_text = re.sub(r'([.!?,])([A-Za-z])', r'\1 \2', fixed_text)
                    # ✅ FINAL FIX: Collapse all whitespace (newlines, tabs, multi-spaces) into one space.
                    yield re.sub(r'\s+', ' ', fixed_text)
        except Exception as e:
            logging.error(f"Error in stream_answer: {e}")
            yield f"ERROR: {str(e)}"