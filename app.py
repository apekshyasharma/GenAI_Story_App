from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from Utils.model_config import setup_gemini_api
from Utils import story_generator

# Load environment variables
load_dotenv(dotenv_path="C:/Users/ghimi/OneDrive/Desktop/Office/GenerativeAI/Utils/.env")
api_key = os.getenv("GEMINI_API_KEY")

# Validate API key
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in environment variables!")
    print("Make sure your .env file contains: GEMINI_API_KEY=your_actual_key")
    exit(1)

# Setup Gemini
try:
    gemini_api = setup_gemini_api(api_key)
    print("Gemini API configured successfully")
except Exception as e:
    print(f"ERROR setting up Gemini: {e}")
    exit(1)

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Story Generator API (Gemini) is running!",
        "endpoints": {
            "generate_story": "/generate-story (POST)",
            "health_check": "/ (GET)"
        }
    })

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "Story Generator API"})

@app.route("/generate-story", methods=["POST"])
def create_story():
    try:
        data = request.get_json()
        required_fields = ["character", "setting", "theme", "age_group"]

        # Validate request data
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "error": f"Missing required fields: {', '.join(missing_fields)}",
                "required_fields": required_fields
            }), 400

        # Generate story
        print(f"Generating story for: {data}")
        generated_story_text = story_generator.create_story(data)
        
        return jsonify({
            "success": True,
            "story": generated_story_text,
            "input_data": data
        })
        
    except Exception as e:
        print(f"Error in create_story endpoint: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == "__main__":
    print("=" * 50)
    print(" Starting Story Generator API...")
    print(" Endpoints available:")
    print("   GET  /          - Home page")
    print("   GET  /health    - Health check")
    print("   POST /generate-story - Generate story")
    print("=" * 50)
    app.run(debug=True, host="0.0.0.0", port=5000)