# Ensure the correct import path for BaseMemory is set
from memory.base_memory import BaseMemory

import chromadb
import uuid
# Uncomment the following imports if custom embeddings and text splitter are needed
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.schema.document import Document


class LongtermSummaryMemory(BaseMemory):
    def __init__(self, db_impl='duckdb+parquet', persist_dir="db_lts", telemetry=False):
        # Initialize settings for ChromaDB
        self.client = chromadb.PersistentClient(path=persist_dir)

        self.collection = self.client.get_or_create_collection(
            "longterm_summary_memory")

        # Initialize embeddings and text splitter if required
        # self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2", model_kwargs={"device": "cpu"})
        # self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=40)

    def store(self, text, metadata=None):
        # Store text summaries and associated metadata into the ChromaDB collection
        document = {"content": text, "metadata": metadata or {}}
        id = str(uuid.uuid4())

        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[id]
        )

    def retrieve(self, query, n_results=1):
        # Retrieve summaries based on a query from the ChromaDB collection
        return self.collection.query(
            query_texts=[query],
            n_results=2)


# Example usage:
if __name__ == "__main__":
    lt_summary_memory = LongtermSummaryMemory()

    # Store summary information
    lt_summary_memory.store("Cardio is a great way to start the weekdays with energy", metadata={
                            "category": "Cardio", "time": "weekday mornings"})

    # Retrieve summaries based on a query
    query = "What is a good weekday morning activity?"
    found_summaries = lt_summary_memory.retrieve(query)
    print(found_summaries)
