from transformers import AutoTokenizer, AutoModel
import torch
import chromadb

# Load the tokenizer and model for embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/paraphrase-MiniLM-L6-v2")

def get_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # Take the average of the output token embeddings (mean pooling)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.squeeze().numpy()

# Example sentence
sentence = "Karthik bought HDFC bank shares"
sentence_embedding = get_embedding(sentence, tokenizer, model)

word_list = ["Karthik", "Dan", "Karthik  HDFC bank"]

# Get embeddings for each word in the list
word_embeddings = [get_embedding(word, tokenizer, model) for word in word_list]


# Initialize ChromaDB client
client = chromadb.Client()

# Create a collection where you will store your word embeddings
collection = client.create_collection("word-check-collection")

# Add the word embeddings to ChromaDB collection
for i, word_embedding in enumerate(word_embeddings):
    collection.add(
        documents=[word_list[i]],  # Store the word as a document
        embeddings=[word_embedding],  # Store the word embedding
        metadatas=[{"word": word_list[i]}],  # Store metadata for each word
        ids=[f"word-{i}"]  # Unique ID for each word
    )

# Search the collection for the top k most similar words
results = collection.query(
    query_embeddings=[sentence_embedding],
    n_results=len(word_list)  # Return all words or top k results
)

# Display the results
for i, result in enumerate(results['documents'][0]):
    word = result
    similarity_score = results['distances'][0][i]  # ChromaDB provides a distance metric
    print(f"Found word '{word}' with similarity score: {similarity_score}")


# Define a similarity threshold (lower is better, as it is a distance score)
threshold = 0.5

# Filter results based on the threshold
for i, distance in enumerate(results['distances'][0]):
    if distance < threshold:
        word = results['documents'][0][i]
        print(f"Word '{word}' is semantically similar to the sentence with distance {distance}")
