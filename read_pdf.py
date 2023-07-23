import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader

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
        # Read a PDF file
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            num_pages = len(reader.pages)
            for page in reader.pages:
                text = page.extract_text()
                print(text)
    else:
        # Read a text file
        with open(file_path, 'r') as file:
            text = file.read()
            print(text)
