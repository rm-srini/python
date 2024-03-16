import openai

# Set your OpenAI API key
api_key = 'APIKEY'

# Initialize the OpenAI API client with your API key
openai.api_key = api_key

# Define your prompt
prompt = "Once upon a time,"

# Generate a completion based on the prompt
response = openai.Completion.create(
    engine="gpt-3.5-turbo-0125",  # specify the engine you want to use
    prompt=prompt,
    max_tokens=50  # specify the maximum number of tokens in the completion
)

# Print the generated completion
print(response['choices'][0]['text'].strip())