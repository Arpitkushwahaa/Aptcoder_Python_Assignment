"""Test Gemini API connection"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key: {api_key[:20]}..." if api_key else "No API key found")

try:
    genai.configure(api_key=api_key)
    
    # List available models
    print("Available models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
    
    # Try using the first available model
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    print("✓ Gemini client configured successfully")
    
    # Test a simple generation
    response = model.generate_content("Say hello")
    print("✓ API call successful!")
    print(f"Response: {response.text}")
    
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
