from videosdk import MeetingConfig, VideoSDK
import asyncio
import os
import jwt
import datetime
from typing import Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Install it with: pip install python-dotenv")
    print("Or set environment variables manually")

# Configuration - you can set these as environment variables or replace with actual values
MEETING_ID = os.getenv('VIDEOSDK_MEETING_ID', 'your-meeting-id-here')
NAME = os.getenv('VIDEOSDK_NAME', 'Participant')
VIDEOSDK_API_KEY = os.getenv('VIDEOSDK_API_KEY', 'your-api-key-here')
VIDEOSDK_SECRET = os.getenv('VIDEOSDK_SECRET', 'your-secret-here')

def generate_token(api_key: str, secret: str, expiry_hours: int = 24) -> str:
    """Generate JWT token from API key and secret"""
    payload = {
        'apikey': api_key,
        'permissions': ['allow_join'],  # permissions for the meeting
        'iat': datetime.datetime.now(datetime.timezone.utc),
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expiry_hours)
    }
    return jwt.encode(payload, secret, algorithm='HS256')

def main():
    # Validate required configuration
    if VIDEOSDK_API_KEY == 'your-api-key-here':
        print("Please set your VIDEOSDK_API_KEY environment variable or update the API key in the code")
        return
    
    if VIDEOSDK_SECRET == 'your-secret-here':
        print("Please set your VIDEOSDK_SECRET environment variable or update the secret in the code")
        return
    
    if MEETING_ID == 'your-meeting-id-here':
        print("Please set your VIDEOSDK_MEETING_ID environment variable or update the meeting ID in the code")
        return
    
    # Generate JWT token from API key and secret
    try:
        token = generate_token(VIDEOSDK_API_KEY, VIDEOSDK_SECRET)
        print("Generated JWT token successfully")
    except Exception as e:
        print(f"Error generating token: {e}")
        return
    
    # Create meeting configuration
    meeting_config = MeetingConfig(
        meeting_id=MEETING_ID,
        name=NAME,
        mic_enabled=True,
        webcam_enabled=True,
        token=token
    )

    # Initialize meeting
    meeting = VideoSDK.init_meeting(**meeting_config)

    # Join the meeting
    meeting.join()
    
    print(f"Joined meeting {MEETING_ID} as {NAME}")

if __name__ == '__main__':
    # Create and run event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        main()
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nLeaving meeting...")
    finally:
        loop.close()