import google.generativeai as genai
import os

def setup_gemini_api(api_key):
    """Configure Gemini API with the provided API key"""
    
    # Validate API key
    if not api_key:
        raise ValueError(
            "Gemini API key not found. Please check your .env file contains: GEMINI_API_KEY=your_key"
        )
    
    if not isinstance(api_key, str) or len(api_key.strip()) < 10:
        raise ValueError("Invalid API key format. Please check your Gemini API key.")
    
    try:
        # Configure the Gemini API
        genai.configure(api_key=api_key.strip())
        
        # Test the connection by listing models
        models = list(genai.list_models())
        print(f" Connected to Gemini API. Available models: {len(models)}")
        
        return genai
        
    except Exception as e:
        raise Exception(f"Failed to configure Gemini API: {e}")

def test_gemini_connection():
    """Test if Gemini API is working properly"""
    try:
        # Try to create a simple model instance
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        
        # Test with a simple prompt
        test_response = model.generate_content("Say 'Hello, I am working!'")
        
        if test_response.text:
            print(" Gemini API test successful!")
            return True, "Connection successful"
        else:
            return False, "No response from Gemini"
            
    except Exception as e:
        return False, f"Connection test failed: {e}"
