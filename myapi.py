from PIL import Image
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

def clean_markdown(text):
    """
    Remove markdown formatting from text to display clean content.
    """
    if not text:
        return ""
    
    # Remove bold **text** and __text__
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'__(.*?)__', r'\1', text)
    
    # Remove italic *text* and _text_
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'_(.*?)_', r'\1', text)
    
    # Remove other markdown patterns
    text = re.sub(r'`(.*?)`', r'\1', text)  # Remove code blocks
    text = re.sub(r'###?\s*(.*?)(?=\n|$)', r'\1', text, flags=re.DOTALL)  # Remove headers
    text = re.sub(r'- \[ \] ', '', text)  # Remove unchecked boxes
    text = re.sub(r'- \[x\] ', '✓ ', text)  # Keep checked boxes as ✓
    
    # Clean up extra newlines and spaces
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Normalize newlines
    text = text.strip()
    
    return text

def get_plant_diagnosis(image_path, prompt):
    """
    Process a plant image and prompt using Gemini API to return a disease diagnosis.
    
    Args:
        image_path (str): Path to the uploaded image (e.g., 'static/uploads/image.jpg')
        prompt (str): User query or default prompt for disease detection
    
    Returns:
        str: Clean AI-generated diagnosis without markdown formatting
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
        
        # Enhanced prompt for cleaner, structured response
        default_prompt = """Analyze this plant image and provide a clear diagnosis:
        nand give a clear disease name in the top of 5 points
1. Plant type (if identifiable)
2. Disease name (if any) or "Healthy"
3. Severity level (Low/Medium/High)
4. Brief treatment recommendations
5. Prevention tips

Respond in simple, clear sentences without using **bold**, *italic*, or other formatting."""

        full_prompt = prompt or default_prompt
        
        # Send image and prompt to Gemini
        response = model.generate_content([
            full_prompt,
            img
        ])
        
        # Clean the response and return
        clean_response = clean_markdown(response.text)
        return clean_response
        
    except Exception as e:
        return f"Error processing image with AI: {str(e)}"