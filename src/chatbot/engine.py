import google.generativeai as genai
import faiss
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from config.settings import (
    GEMINI_API_KEY, GEMINI_MODEL, MAX_TOKENS, TEMPERATURE, 
    TOP_K_RESULTS, MAX_CONTEXT_LENGTH, SUBREDDIT_NAME,
    DATA_PROCESSED_PATH, EMBEDDINGS_PATH
)
from config.prompts import SYSTEM_PROMPT_TEMPLATE, SAFETY_PROMPT
from .utils import clean_text, truncate_text

class GeminiChatbot:
    def __init__(self):
        self.subreddit = SUBREDDIT_NAME
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(
            GEMINI_MODEL,
            generation_config=genai.GenerationConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_TOKENS
            ),
            safety_settings={
                'HATE': 'block_none',
                'HARASSMENT': 'block_none',
                'SEXUAL': 'block_none',
                'DANGEROUS': 'block_none'
            }
        )
        
        # Load FAISS index and corpus
        index_path = os.path.join(EMBEDDINGS_PATH, "reddit_index.faiss")
        corpus_path = os.path.join(DATA_PROCESSED_PATH, "corpus.json")
        
        self.index = faiss.read_index(index_path)
        with open(corpus_path) as f:
            self.corpus = json.load(f)

    def _retrieve_context(self, query: str, k: int = TOP_K_RESULTS) -> list[str]:
        """Retrieve top-k most relevant context chunks"""
        query_embedding = self.embedder.encode([clean_text(query)])
        distances, indices = self.index.search(query_embedding, k)
        return [truncate_text(self.corpus[i], MAX_CONTEXT_LENGTH) for i in indices[0]]

    def generate_response(self, query: str) -> str:
        """Generate response using Gemini API"""
        context_chunks = self._retrieve_context(query)
        context_str = "\n\n".join([f"• {chunk}" for chunk in context_chunks])
        
        # Construct prompt for Gemini
        full_prompt = (
            SAFETY_PROMPT + 
            SYSTEM_PROMPT_TEMPLATE.format(
                subreddit=self.subreddit,
                context=context_str
            ) +
            f"\n\n**User Question:** {query}"
        )
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def chat(self):
        """Interactive chat interface"""
        print(f"Welcome to the r/{self.subreddit} chatbot! Type 'exit' to end.")
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            response = self.generate_response(user_input)
            print(f"\nBot: {response}")

if __name__ == "__main__":
    bot = GeminiChatbot()
    bot.chat()