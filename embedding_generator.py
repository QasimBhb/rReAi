from sentence_transformers import SentenceTransformer
import numpy as np
import json
import faiss

def create_embeddings(dataset_path):
    with open(dataset_path) as f:
        data = json.load(f)
    
    # Combine all text
    corpus = []
    for post in data:
        corpus.append(post["title"])
        corpus.append(post["text"])
        corpus.extend(post["comments"])
    
    # Generate embeddings
    model = SentenceTransformer('all-mpnet-base-v2')  # High-quality embeddings
    embeddings = model.encode(corpus, show_progress_bar=True)
    
    # Create FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    
    # Save index and corpus
    faiss.write_index(index, "reddit_index.faiss")
    with open("corpus.json", "w") as f:
        json.dump(corpus, f)