import json
import os
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import faiss
from config.settings import DATA_RAW_PATH, DATA_PROCESSED_PATH, EMBEDDINGS_PATH
from src.chatbot.utils import clean_text

def generate_embeddings(input_path: str) -> None:
    """Generate embeddings and FAISS index from scraped data"""
    with open(input_path) as f:
        data = json.load(f)
    
    # Extract text: post titles, post texts, and comment bodies
    corpus = []
    for post in data:
        corpus.append(clean_text(post['title']))
        if post['text'].strip():
            corpus.append(clean_text(post['text']))
        for comment in post['comments']:
            corpus.append(clean_text(comment['body']))
    
    # Remove duplicates and empty strings
    corpus = list(set([text for text in corpus if text.strip()]))
    print(f"Generated {len(corpus)} unique text chunks")
    
    # Load model and generate embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(corpus, show_progress_bar=True, batch_size=32)
    
    # Create FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))
    
    # Ensure output directories exist
    os.makedirs(DATA_PROCESSED_PATH, exist_ok=True)
    os.makedirs(EMBEDDINGS_PATH, exist_ok=True)
    
    # Save corpus and index
    corpus_path = os.path.join(DATA_PROCESSED_PATH, "corpus.json")
    index_path = os.path.join(EMBEDDINGS_PATH, "reddit_index.faiss")
    
    with open(corpus_path, 'w') as f:
        json.dump(corpus, f)
    
    faiss.write_index(index, index_path)
    print(f"Saved index to {index_path} and corpus to {corpus_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate embeddings from scraped data')
    parser.add_argument('--input', type=str, required=True, help='Path to scraped JSON file')
    args = parser.parse_args()
    
    generate_embeddings(args.input)