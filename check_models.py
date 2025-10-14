#  This file is purely for printing which AI Models you have available to you 
# to use with the program, allowing you to edit the Generative Model

import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY") # Insert your API Key for Google Gemini here
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name) # Print all models available with your billing plan