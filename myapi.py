from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

def generate_with_image():
    # Model select kar
    model = genai.GenerativeModel("gemini-2.0-flash")

    # Image load kar
    img = Image.open(os.path.join('images','2.png')) 

    # Text + Image dono send kar
    response = model.generate_content([
        "which plant desease in this?",
        img
    ])

    print(response.text)

if __name__ == "__main__":
    generate_with_image()
