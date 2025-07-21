#!/usr/bin/env python3
"""
Generate a JWT token for the VideoSDK web interface
"""

import os
import jwt
import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

VIDEOSDK_API_KEY = os.getenv('VIDEOSDK_API_KEY', 'your-api-key-here')
VIDEOSDK_SECRET = os.getenv('VIDEOSDK_SECRET', 'your-secret-here')

def generate_token(api_key: str, secret: str, expiry_hours: int = 24) -> str:
    """Generate JWT token from API key and secret"""
    payload = {
        'apikey': api_key,
        'permissions': ['allow_join'],
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expiry_hours)
    }
    return jwt.encode(payload, secret, algorithm='HS256')

if __name__ == "__main__":
    if VIDEOSDK_API_KEY == 'your-api-key-here' or VIDEOSDK_SECRET == 'your-secret-here':
        print("❌ Please set your VIDEOSDK_API_KEY and VIDEOSDK_SECRET in the .env file")
    else:
        try:
            token = generate_token(VIDEOSDK_API_KEY, VIDEOSDK_SECRET)
            print("✅ Generated JWT Token:")
            print(token)
            print("\n💡 Copy this token and paste it in the index.html file (TOKEN variable)")
        except Exception as e:
            print(f"❌ Error generating token: {e}")
