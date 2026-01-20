"""Test OpenAI API connection"""
import os
from dotenv import load_dotenv
import openai

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key found: {api_key[:20]}..." if api_key else "No API key")

try:
    client = openai.OpenAI(api_key=api_key)
    print("✓ OpenAI client created successfully")
    
    # Test a simple completion
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Say hello"}
        ],
        max_tokens=10
    )
    print("✓ API call successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
