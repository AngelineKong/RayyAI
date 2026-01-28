"""
Test script to check available Gemini models and test vision capability
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv()

# Configure API
api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key found: {bool(api_key)}")

if api_key:
    genai.configure(api_key=api_key)

    print("\n=== Available Gemini Models ===")
    try:
        models = genai.list_models()

        vision_models = []
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"\n[OK] {model.name}")
                print(f"   Supported: {', '.join(model.supported_generation_methods)}")

                # Check if it's a vision model
                if 'vision' in model.name.lower() or 'flash' in model.name.lower() or 'pro' in model.name.lower():
                    vision_models.append(model.name)

        print("\n\n=== Recommended Models for Vision ===")
        if vision_models:
            for vm in vision_models:
                print(f"  • {vm}")
        else:
            print("  Looking for models with 'flash', 'pro', or 'vision' in name")

        # Test if gemini-2.0-flash-exp is available
        print("\n\n=== Testing gemini-2.0-flash-exp ===")
        try:
            test_model = genai.GenerativeModel('gemini-2.0-flash-exp')
            print("[OK] gemini-2.0-flash-exp is available!")
        except Exception as e:
            print(f"[ERROR] gemini-2.0-flash-exp error: {e}")

            # Try alternative
            print("\n=== Trying alternative: gemini-1.5-flash ===")
            try:
                test_model = genai.GenerativeModel('gemini-1.5-flash')
                print("[OK] gemini-1.5-flash is available!")
            except Exception as e2:
                print(f"[ERROR] gemini-1.5-flash error: {e2}")

    except Exception as e:
        print(f"Error: {e}")
else:
    print("No API key found in .env file")
