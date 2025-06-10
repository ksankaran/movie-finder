import os
import httpx
from pinecone import Pinecone
from langchain_openai import AzureOpenAIEmbeddings

pc = Pinecone(api_key=os.getenv("PINECONE_KEY"), ssl_verify=False)

index_name = "wiki-movies"
index = pc.Index(index_name)

def main():
    print("Hello from movie-finder!")
    params = {
        "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
        "azure_deployment": os.getenv("AZURE_EMBED_DEPLOYMENT"),
        "api_version": os.getenv("EMBED_API_VERSION"),
        "api_key": os.getenv("AZURE_API_KEY"),
        "timeout": 60,
        "http_client": httpx.Client(verify=False),
    }
    client = AzureOpenAIEmbeddings(**params)
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
