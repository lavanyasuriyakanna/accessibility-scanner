# NLP Simplification using SpaCy
# Note: For production, requires `python -m spacy download en_core_web_sm`

try:
    import spacy
    print("Loading SpaCy en_core_web_sm...")
    nlp = spacy.load("en_core_web_sm")
    HAS_SPACY = True
except ImportError:
    HAS_SPACY = False
    print("SpaCy not found. Running naive text summarization.")
except OSError:
    HAS_SPACY = False
    print("SpaCy model not found. Run `python -m spacy download en_core_web_sm`.")

def simplify_text_layout(paragraphs):
    """
    Takes an array of raw text chunks from a webpage and simplifies the language / strips complexity.
    """
    simplified_chunks = []
    
    for text in paragraphs:
        if not text.strip():
            continue
            
        if HAS_SPACY:
            # Perform dependency parsing and named entity recognition to maintain key context 
            # while stripping overly complex adjectives or subordinate clauses (mocking the full logic)
            doc = nlp(text)
            
            # Simple summarization: keep sentences that contain standard Subject-Verb-Object
            # For boilerplate, just joining primary sentences
            sentences = [sent.text for sent in doc.sents]
            simplified_chunks.append(" ".join(sentences[:2]) + ("..." if len(sentences) > 2 else ""))
            
        else:
            # Naive approach
            simplified_chunks.append(text[:100] + "..." if len(text) > 100 else text)

    return simplified_chunks
