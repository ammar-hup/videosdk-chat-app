#!/usr/bin/env python3
"""
Utility script to test VideoSDK API credentials and create meetings
"""

import os
import jwt
import requests
import datetime
import json

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Install it with: pip install python-dotenv")

VIDEOSDK_API_KEY = os.getenv('VIDEOSDK_API_KEY', 'your-api-key-here')
VIDEOSDK_SECRET = os.getenv('VIDEOSDK_SECRET', 'your-secret-here')

def generate_token(api_key: str, secret: str, expiry_hours: int = 24) -> str:
    """Generate JWT token from API key and secret"""
    payload = {
        'apikey': api_key,
        'permissions': ['allow_join'],  # Basic permission for joining
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expiry_hours)
    }
    return jwt.encode(payload, secret, algorithm='HS256')

def create_meeting(token: str) -> str:
    """Create a new meeting room and return the room ID"""
    url = "https://api.videosdk.live/v2/rooms"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        room_data = response.json()
        return room_data.get('roomId')
    else:
        print(f"Error creating meeting: {response.status_code} - {response.text}")
        return None

def test_credentials():
    """Test if the API credentials are valid"""
    if VIDEOSDK_API_KEY == 'your-api-key-here' or VIDEOSDK_SECRET == 'your-secret-here':
        print("❌ Please set your VIDEOSDK_API_KEY and VIDEOSDK_SECRET in the .env file")
        return False
    
    try:
        # Generate token
        token = generate_token(VIDEOSDK_API_KEY, VIDEOSDK_SECRET)
        print("✅ JWT token generated successfully")
        
        # Test by creating a meeting
        room_id = create_meeting(token)
        if room_id:
            print(f"✅ Meeting created successfully! Room ID: {room_id}")
            print(f"You can use this Room ID as your VIDEOSDK_MEETING_ID")
            return True
        else:
            print("❌ Failed to create meeting - check your credentials")
            return False
            
    except Exception as e:
        print(f"❌ Error testing credentials: {e}")
        return False

if __name__ == "__main__":
    print("VideoSDK Credential Tester")
    print("=" * 30)
    
    if test_credentials():
        print("\n🎉 Your VideoSDK credentials are working correctly!")
    else:
        print("\n💡 Please check your API key and secret from https://app.videosdk.live/dashboard")
