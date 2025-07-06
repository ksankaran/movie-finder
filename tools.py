from typing import Any
from langchain_core.tools import tool
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

pc = Pinecone()

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
    client = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        api_version="2024-10-21"
    )
    embeddings = client.embed_query(query)
    results = index.query(
        vector=embeddings,
        top_k=20,
        include_values=False,
        include_metadata=True
    )
    output = []
    for match in results.matches:
        output.append(f"Score: {match.score}, Movie Name: {match.metadata['name']}, URL: {match.metadata['url']}, PLOT: {match.metadata['plot']}")
    return "\n".join(output) if output else "No results found."