import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader
import nltk
from nltk.stem import PorterStemmer
import requests


def pdf_text_generator(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            yield text


# Replace 'YOUR_OPENAI_API_KEY' with your actual API key
API_KEY = 'API_KEY'

# Create a Tkinter root window
root = tk.Tk()

# Hide the root window
root.withdraw()

# Open the file explorer dialog
file_path = filedialog.askopenfilename()

# Check if a file was selected
if file_path:
    # Determine the file extension
    file_extension = file_path.split('.')[-1]

    if file_extension.lower() == 'pdf':
        # Initialize tqdm progress bar
        with tqdm(total=1, desc="Importing PDF") as pbar:
            # Tokenize and stem the text incrementally
            tokens = []
            stemmer = PorterStemmer()
            for page_text in pdf_text_generator(file_path):
                page_tokens = nltk.word_tokenize(page_text)
                stemmed_tokens = [stemmer.stem(token) for token in page_tokens]
                tokens.extend(stemmed_tokens)
                pbar.update(1)

    else:
        # Read a text file
        with open(file_path, 'r') as file:
            text = file.read()

            # Tokenize and stem the text
            tokens = nltk.word_tokenize(text)
            stemmer = PorterStemmer()
            tokens = [stemmer.stem(token) for token in tokens]

    print("Bot: Hello! How can I assist you today?")
    while True:
        # Get user input
        user_input = input("User: ")

        # Tokenize and stem user input
        user_tokens = nltk.word_tokenize(user_input)
        stemmer = PorterStemmer()
        user_stemmed_tokens = [stemmer.stem(token) for token in user_tokens]

        # Search for matching tokens in the source text
        matching_tokens = [
            token for token in user_stemmed_tokens if token in tokens]

        if matching_tokens:
            # Make API call to GPT-3
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}'
            }
            prompt = f"User: {user_input}\nBot:"
            data = {
                'prompt': prompt,
                'temperature': 0.7,
                'max_tokens': 50
            }
            response = requests.post(
                'https://api.openai.com/v1/engines/davinci/completions', headers=headers, json=data)
            response_data = response.json()
            print(f"response_data: {response_data}")
            choices = response_data.get('choices', [])
            if choices:
                response_text = choices[0]['text'].strip()
            else:
                response_text = "I'm sorry, I don't have the information you're looking for."

            print("Bot:", response_text)
        else:
            # No matching tokens found
            response = "I'm sorry, I don't have the information you're looking for."

            print("Bot:", response)
