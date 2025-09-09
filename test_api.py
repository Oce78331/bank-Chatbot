import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

def test_chroma_query(query: str):
    # Initialize persistent client
    client = chromadb.PersistentClient(path="./chroma_db")

    # Same embedding model as rag_service.py
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    # Load the collection
    collection = client.get_or_create_collection(
        name="banking_docs", embedding_function=ef
    )

    # Run query
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    print(f"\n🔍 Query: {query}")
    print("📄 Top Results:")
    for i, doc in enumerate(results.get("documents", [[]])[0]):
        print(f"{i+1}. {doc}")


if __name__ == "__main__":
    # Example queries
    test_chroma_query("What is the savings account interest rate?")
    test_chroma_query("How do I check recent transactions?")
    test_chroma_query("Tell me about loan options.")
