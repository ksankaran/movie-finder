import httpx
import os
from typing import Any
from langchain_core.tools import tool
from pinecone import Pinecone
from langchain_openai import AzureOpenAIEmbeddings

pc = Pinecone(api_key=os.getenv("PINECONE_KEY"), ssl_verify=False)

index_name = "wiki-movies"
index = pc.Index(index_name)

@tool(description="Search movies using vector embeddings. Provide a query string to find relevant movies.")
def search_movies_using_vector(query: str) -> str:
    """
    Get vector from query using Azure OpenAI Embeddings.
    
    Args:
        query (str): The query string to embed.
    
    Returns:
        Any: The embedded vector representation of the query.
    """
    params = {
        "azure_endpoint": os.getenv("AZURE_ENDPOINT"),
        "azure_deployment": os.getenv("AZURE_EMBED_DEPLOYMENT"),
        "api_version": os.getenv("EMBED_API_VERSION"),
        "api_key": os.getenv("AZURE_API_KEY"),
        "timeout": 60,
        "http_client": httpx.Client(verify=False),
    }
    client = AzureOpenAIEmbeddings(**params)
    embeddings = client.embed_query(query)
    results = index.query(
        vector=embeddings,
        top_k=10,
        include_values=False,
        include_metadata=True
    )
    output = []
    for match in results.matches:
        output.append(f"Score: {match.score}, Movie Name: {match.metadata["name"]}, URL: {match.metadata["url"]}, PLOT: {match.metadata["plot"]}")
    return "\n".join(output) if output else "No results found."