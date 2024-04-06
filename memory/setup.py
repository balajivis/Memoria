import chromadb
from chromadb.config import Settings


client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                  persist_directory="db/"
                                  ))

collection = client.create_collection(name="longterm_summary_memory")

collection = client.create_collection(name="associative_memory")
