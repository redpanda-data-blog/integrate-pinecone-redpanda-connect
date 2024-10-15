import sys
from pinecone.grpc import PineconeGRPC as Pinecone
from sentence_transformers import SentenceTransformer
import warnings
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index(os.getenv('PINECONE_INDEX'))

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode(text).tolist()

def check_comment(comment):
    # Generate embedding for the input comment
    embedding = get_embedding(comment)
    
    # Query Pinecone index
    results = index.query(vector=embedding, top_k=5, include_metadata=True)

    # Count harmful and non-harmful matches
    harmful_count = sum(1 for match in results['matches'] if match['metadata'].get('is_harmful', True))

    non_harmful_count = len(results['matches']) - harmful_count
    
    # Determine if the comment is harmful based on majority
    is_harmful = harmful_count > non_harmful_count
    
    return is_harmful

if __name__ == "__main__":
    # Prompt the user for input
    comment = input("Please enter a comment to check: ")
    result = check_comment(comment)
    
    if result:
        print("The comment is considered harmful.")
    else:
        print("The comment is considered non-harmful.")
