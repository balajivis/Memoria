from memory.base_memory import BaseMemory

import chromadb
from chromadb.config import Settings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document


class AssociativeMemory(BaseMemory):
    def __init__(self, db_impl='duckdb+parquet', persist_dir="db", telemetry=False):
        # Initialize settings for ChromaDB
        self.client = chromadb.Client(Settings(
            chroma_db_impl=db_impl,
            persist_directory=persist_dir,
            anonymized_telemetry=telemetry
        ))
        self.collection = self.client.create_collection(name="Preferences")

        # We will use th default embeddings and text splitter for now, later we can change this to below

        # self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs={"device": "cpu"})
        # self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)

    def store(self, user_preferences, metadata):
        # This function would take a list of user preferences, turn them into documents
        # and store them in the ChromaDB
        self.setup_db(user_preferences)
        self.collection.add(
            documents=[user_preferences],
            metadatas=[metadata]
        )

    def retrieve(self, query):
        return self.collection.query(
            query_texts=[query],
            n_results=2)


# Example usage:
if __name__ == "__main__":
    associative_memory = AssociativeMemory()

    # Store preferences
    user_preferences = ["Cardio on weekdays",
                        "Yoga on weekends", "Gym in the evenings"]
    associative_memory.store(user_preferences)

    # Retrieve a preference based on a query
    query = "I want to relax"
    found_preferences = associative_memory.retrieve(query)
    print(found_preferences)
