from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

pc = Pinecone()

index_name = "wiki-movies"
index = pc.Index(index_name)

def main():
    print("Hello from movie-finder!")
    client = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_version="2024-10-21"
    )
    query_embed = client.embed_query("hero name is matrix and he worked in army")
    print(f"Query embedding: {query_embed[:10]}...")
    results = index.query(
        vector=query_embed,
        top_k=10,
        include_values=False,
        include_metadata=True
    )
    print("Results:")
    for match in results.matches:
        print(f"Score: {match.score}, Metadata: {match.metadata}")

if __name__ == "__main__":
    main()
