import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def setup_chroma():
    """Initializes ChromaDB and populates it with sample banking documents."""
    try:
        print("🚀 Starting ChromaDB setup...")
        
        # Initialize a persistent client
        print("📁 Creating ChromaDB client...")
        client = chromadb.PersistentClient(path="./chroma_db")
        print("✅ ChromaDB client created")
        
        # Use the same embedding model as the RAG service
        print("🧠 Creating embedding function...")
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        print("✅ Embedding function created")

        # Get or create the collection
        print("📚 Creating/accessing collection...")
        collection = client.get_or_create_collection(
            name="banking_docs", embedding_function=ef
        )
        print("✅ Collection ready")

        # --- Clear existing documents to prevent duplicates on re-running ---
        print("🧹 Clearing existing documents...")
        existing_docs = collection.get()
        if existing_docs['ids']:
            collection.delete(ids=existing_docs['ids'])
            print(f"✅ Cleared {len(existing_docs['ids'])} existing documents.")
        else:
            print("✅ No existing documents to clear.")

        # Sample banking documents for the knowledge base
        print("📄 Preparing banking documents...")
        documents = [
            "The Platinum Savings Account offers a competitive 2.5% annual interest rate on balances exceeding $10,000. A minimum balance of $1,000 is required to avoid a monthly maintenance fee of $10.",
            "Our Basic Checking Account is completely free, with no monthly fees or minimum balance requirements. It also includes complimentary online bill pay and a debit card.",
            "ocean Bank offers personal loans with interest rates starting as low as 5.99% APR. Repayment terms are flexible, ranging from 24 to 60 months, depending on your creditworthiness.",
            "Applying for a mortgage is simple. We offer both fixed-rate and variable-rate options. A minimum credit score of 620 is typically required to qualify for our best rates.",
            "Our customer service center is available to help you 24/7. You can reach us by calling 1-800-5642-4541, emailing support@oceanbank.com, or using the live chat feature in our mobile app.",
            "Your security is our top priority. We utilize multi-factor authentication and state-of-the-art encryption to safeguard your personal and financial information.",
            "The Ocean Bank mobile app provides secure access to your accounts using fingerprint or face recognition. You can check balances, deposit checks, and transfer funds with just a few taps.",
            "You can easily view your transaction history for the last 24 months through our online banking portal or directly in the mobile app. Statements are generated monthly."
        ]
        print(f"✅ Prepared {len(documents)} banking documents")

        # Add the documents to the collection
        print("💾 Adding documents to collection...")
        ids = [f"doc_{i+1}" for i in range(len(documents))]
        collection.add(documents=documents, ids=ids)
        print("✅ Documents added successfully")

        print(f"🎉 ChromaDB setup complete! Inserted {len(documents)} documents into the 'banking_docs' collection.")
        
    except Exception as e:
        print(f"❌ Error during ChromaDB setup: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    setup_chroma()
