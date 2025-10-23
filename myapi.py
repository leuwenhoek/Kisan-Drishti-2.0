from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

def get_plant_diagnosis(image_path, prompt):
    """
    Process a plant image and prompt using Gemini API to return a disease diagnosis.
    
    Args:
        image_path (str): Path to the uploaded image (e.g., 'static/uploads/image.jpg')
        prompt (str): User query or default prompt for disease detection
    
    Returns:
        str: AI-generated diagnosis or error message
    """
    try:
        # Load environment variables
        load_dotenv()
        api_key = os.getenv("API_KEY")
        if not api_key:
            return "Error: API_KEY not found in .env file"
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Load image with PIL
        img = Image.open(image_path)
        
        # Initialize Gemini model
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Send image and prompt to Gemini
        response = model.generate_content([
            prompt or "What plant disease is shown in this image? If no disease is detected, describe the plant's health.",
            img
        ])
        
        # Return the AI-generated diagnosis
        return response.text
    except Exception as e:
        return f"Error processing image with AI: {str(e)}"