"""
Text processing utilities for improved LLM response formatting.
"""

import re
from typing import List, Dict, Any, Optional, Set

def clean_text(text: str) -> str:
    """
    Clean up text by fixing spaces around punctuation and handling contractions properly.
    
    Addresses common detokenization issues from LLM outputs:
    - Removes extra spaces before punctuation
    - Fixes contractions like "don 't" -> "don't"
    - Fixes spacing around parentheses and brackets
    - Removes double spaces
    - Ensures proper spacing around quotation marks
    - Fixes ellipsis formatting
    - Preserves URLs and email addresses
    - Handles multi-punctuation like "?!"
    
    Args:
        text: The input text to clean
        
    Returns:
        str: The cleaned text with proper spacing and formatting
    """
    # Preserve URLs and email addresses first (protect them from other replacements)
    url_pattern = r'(https?://[^\s]+)'
    email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'
    
    # Extract URLs and emails with unique placeholders
    urls = re.findall(url_pattern, text)
    emails = re.findall(email_pattern, text)
    
    # Replace with placeholders
    for i, url in enumerate(urls):
        text = text.replace(url, f"___URL{i}___")
        
    for i, email in enumerate(emails):
        text = text.replace(email, f"___EMAIL{i}___")
    
    # Fix spaces before punctuation (but not in multi-punctuation like ?!)
    text = re.sub(r'\s+([,.!?:;])', r'\1', text)
    
    # Fix multi-punctuation spacing (e.g. "! ?" -> "!?")
    text = re.sub(r'([!?])\s+([!?])', r'\1\2', text)
    
    # Fix spaces in contractions - make sure to handle both straight and curly apostrophes
    text = re.sub(r"(\w+)\s+n['']t", r"\1n't", text)
    text = re.sub(r"(\w+)\s+['']s", r"\1's", text)
    text = re.sub(r"(\w+)\s+['']re", r"\1're", text)
    text = re.sub(r"(\w+)\s+['']ve", r"\1've", text)
    text = re.sub(r"(\w+)\s+['']ll", r"\1'll", text)
    text = re.sub(r"(\w+)\s+['']d", r"\1'd", text)
    text = re.sub(r"(\w+)\s+['']m", r"\1'm", text)
    
    # Fix spaces around parentheses and brackets
    text = re.sub(r'\s+\)', ')', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+]', ']', text)
    text = re.sub(r'\[\s+', '[', text)
    
    # Fix spacing around quotation marks (both single and double, straight and curly)
    # First, fix patterns like 'word " word' and 'word " .'
    text = re.sub(r'(\w)\s+(["\'])', r'\1\2', text)
    # Fix patterns like '" word' and "' ."  
    text = re.sub(r'(["\'])\s+(\w)', r'\1\2', text)
    # Don't remove spaces around quotes that are between words (e.g., word " word -> word " word)
    # This preserves quotes used in dialogue
    
    # Fix ellipsis (ensure no spaces between dots)
    text = re.sub(r'\.+\s+\.+', '...', text)
    text = re.sub(r'\.\s+\.\s+\.', '...', text)
    
    # Fix double spaces
    text = re.sub(r'\s{2,}', ' ', text)
    
    # Ensure space after sentence-ending punctuation (if followed by a letter or digit)
    text = re.sub(r'([.!?])([a-zA-Z0-9])', r'\1 \2', text)
    
    # Restore URLs and emails from placeholders
    for i, url in enumerate(urls):
        text = text.replace(f"___URL{i}___", url)
        
    for i, email in enumerate(emails):
        text = text.replace(f"___EMAIL{i}___", email)
    
    return text


def tokenize(text: str) -> List[str]:
    """
    Split text into tokens (simple whitespace-aware word tokenization).
    
    Args:
        text: Text to tokenize
        
    Returns:
        List of tokens
    """
    return re.findall(r'\b\w+\b', text.lower())


def filter_stopwords(tokens: List[str], stopwords: Set[str]) -> List[str]:
    """
    Remove stopwords from a list of tokens.
    
    Args:
        tokens: List of tokens to filter
        stopwords: Set of stopwords to remove
        
    Returns:
        List of tokens with stopwords removed
    """
    return [t for t in tokens if t not in stopwords]
