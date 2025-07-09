import re
import html

def clean_text(text: str) -> str:
    """Clean text by removing URLs, special characters, and HTML entities"""
    # Decode HTML entities
    text = html.unescape(text)
    
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    
    # Remove Reddit markdown links
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove special characters except basic punctuation
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to a maximum length without cutting words"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + " [...]"