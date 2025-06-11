# Scene to Screen: A RAG-Powered Movie Finder

Find films by describing scenes or plot points using semantic search and large language models.

## About

Movie Finder is an AI-powered application that helps you identify movies based on your descriptions of scenes, plot elements, or character moments. Unlike traditional keyword search, this tool uses Retrieval-Augmented Generation (RAG) to understand the semantic meaning behind your descriptions.

Have you ever thought "What's that movie where people enter dreams to steal ideas?" or "The one with the upside-down kiss in the rain?" - Movie Finder can help!

## Features

- **Natural Language Search**: Describe scenes, plots, or moments in your own words
- **Semantic Understanding**: Goes beyond keyword matching to understand concepts
- **Conversational Interface**: Ask follow-up questions and refine your search
- **Comprehensive Movie Database**: Powered by a vector database of movie plot summaries

## Technology Stack

- **LangGraph**: For orchestrating the conversational agent workflow
- **LangChain**: For building the RAG pipeline
- **Pinecone**: Vector database for storing and querying movie embeddings
- **OpenAI Embeddings**: For converting text to semantic vector representations
- **OpenAI LLM**: GPT-4.1-mini for understanding queries and generating responses

## Architecture

The system is built around a RAG (Retrieval-Augmented Generation) architecture:

1. **Vector Database**: Movie plots are embedded and stored in Pinecone
2. **Semantic Search**: User queries are converted to embeddings and matched against the database
3. **LLM Processing**: The language model evaluates search results and generates helpful responses
4. **Conversation Management**: The system maintains context for follow-up questions

## How It Works

### Vector Database Setup

The `insert_vectors.py` script:
- Creates a Pinecone index for movie data
- Reads movie plots from a CSV file
- Converts plot descriptions to embeddings using OpenAI's model
- Uploads vectors with metadata to Pinecone

### Search Processing Flow

1. User submits a natural language query describing a movie
2. The query is processed by the LangGraph agent
3. The embedding model converts the query to a vector representation
4. The vector is compared against the movie database using semantic similarity
5. The most relevant movie matches are retrieved
6. The LLM evaluates the results and generates a helpful response
7. The user receives information about the most likely movie matches

## Setup Instructions

### Prerequisites

- Python 3.13+
- Pinecone API key
- OpenAI API key

### Installation

1. Clone this repository:
```bash
git clone https://github.com/ksankaran/movie-finder.git
cd movie-finder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export PINECONE_API_KEY="your-pinecone-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

### Setting Up the Vector Database

To initialize the movie database:

```bash
python setup/insert_vectors.py
```

### Running the Application

Start the application with:

```bash
python app.py
```

## Usage Examples

### Example 1: Finding a Movie by Plot Description

**User**: "I'm looking for a movie where a man plants ideas in other people's dreams"

**System**: "Based on your description, you're likely looking for 'Inception' (2010), directed by Christopher Nolan. It follows Dom Cobb (Leonardo DiCaprio), who specializes in entering people's dreams to extract information, but is tasked with planting an idea into someone's mind instead."

### Example 2: Finding a Movie by Scene Description

**User**: "What's that movie with the upside-down kiss in the rain?"

**System**: "That famous scene is from 'Spider-Man' (2002), directed by Sam Raimi. The upside-down kiss in the rain happens between Spider-Man (Tobey Maguire) and Mary Jane Watson (Kirsten Dunst) after he saves her from attackers in an alley."

## Future Enhancements

- Add support for TV shows and other media
- Implement multimodal search to find movies based on described visual elements
- Incorporate user feedback to improve search quality
- Expand metadata to include actors, directors, and genres

## License

MIT License

## Acknowledgments

- This project uses data derived from public movie plot descriptions
- Built with LangChain and LangGraph