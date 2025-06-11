import os
import httpx
import csv
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

script_dir = Path(__file__).resolve().parent

pc = Pinecone(api_key=os.getenv("PINECONE_KEY"), ssl_verify=False)
index_name = "wiki-movies"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

client = OpenAIEmbeddings(
    model="text-embedding-ada-002",
    api_version="2024-10-21"
)

# embeds = client.embed_documents(
#     [
#         "The plot is set in 1935, during the Depression. Max Brown (Bud Cort) is an urban east-province Canadian fresh from college who travels to Western Canada to accept a teaching position at a one-room rural schoolhouse in the fictional settlement of Willowgreen, Saskatchewan, because there are no other jobs available. He decides to live in the school's basement, having to adapt to teaching in the Depression-era rural setting, especially given the bleakness of the settlement. His students at first are rebellious, but it eventually changes to a connection between student and teacher as Max gets into a love for Alice Field (played by Samantha Eggar), going to him for emotional support. Max barely gets paid and he suffers through the paltry winter of Willowgreen, especially suffering given his physical and emotional isolation in the town, only finding solace in Harris Montgomery (played by Gary Reineke) and Alice Field, who both try to use him to solve their problems of political socialism and her being a war bride of Britain. Max eventually begins to understand Willowgreen and the rural struggles, as the inspector (Kenneth Griffith) comes in to look at his work, which does not end too well. The school year ends as Max is getting on a train back east, but before the credits roll, he tells us he returned the following September to teach another year at Willowgreen."
#     ]
# )
# for vector in embeds:
#     print(str(vector)[:100])

def get_chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
    
plot_file = script_dir / 'assets/plots.csv'
with open(plot_file, 'r', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter='|')
    all_data = [(index, data) for index, data in enumerate(reader)]
    print(str(all_data)[:100])
    chunks = get_chunks(all_data, 100)
    for chunk in chunks:
        if chunk[-1][0] < 41799:
            continue
        print(f"Processing chunk ending with index {chunk[-1][0]}")
        ids = [str(index) for index, _ in chunk]
        names = [data[0] for _, data in chunk]
        urls = [data[1] for _, data in chunk]
        texts = [data[2] for _, data in chunk]
        embeds = client.embed_documents(texts)
        vectors = [
            {
                "id": "id-" + id_,
                "values": embed,
                "metadata": {
                    "url": url,
                    "name": name,
                    "plot": text
                },
            }
            for id_, embed, text, url, name in zip(ids, embeds, texts, urls, names)
        ]
        print(f"Inserting {len(vectors)} vectors into the index {index_name}...")
        pc.Index(index_name).upsert(vectors=vectors)
        print(f"Inserted {len(vectors)} vectors into the index.")