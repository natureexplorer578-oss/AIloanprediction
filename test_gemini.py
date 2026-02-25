from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print("API KEY FOUND:", bool(api_key))

if not api_key:
    raise RuntimeError("API key not found")

# Create Gemini client
client = genai.Client(api_key=api_key)

# ✅ USE SUPPORTED MODEL FROM YOUR LIST
response = client.models.generate_content(
    model="models/gemini-flash-latest",
    contents="Say hello and confirm the API key is working"
)

print("RESPONSE:")
print(response.text)