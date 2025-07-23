from agora_token_builder import RtcTokenBuilder
import time
import os
import http.server
import socketserver
from http import HTTPStatus
from string import Template
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Replace with your Agora credentials
APP_ID = os.getenv('AGORA_APP_ID', 'your-api-key-here')
APP_CERTIFICATE = os.getenv('AGORA_APP_CERTIFICATE', 'your-secret-here')
CHANNEL_NAME = os.getenv('AGORA_CHANNEL_NAME', 'testChannel')
PORT = 8001  # Different from VideoSDK port

def generate_agora_token(uid=0):
    current_time = int(time.time())
    expire_timestamp = current_time + 3600  # 1 hour
    
    token = RtcTokenBuilder.buildTokenWithUid(
        APP_ID, APP_CERTIFICATE, CHANNEL_NAME, uid, 1, expire_timestamp
    )
    return token

class AgoraHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # Generate a token
            token = generate_agora_token()
            
            # Read the HTML template
            with open(os.path.join(os.path.dirname(__file__), 'web', 'agora-enhanced.html'), 'r') as file:
                html_content = file.read()
            
            # Replace placeholders with actual values
            html_content = html_content.replace('YOUR_APP_ID', APP_ID)
            html_content = html_content.replace('YOUR_TOKEN_FROM_BACKEND', token)
            html_content = html_content.replace('testChannel', CHANNEL_NAME)
            
            # Send response
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            # Serve other files normally
            super().do_GET()
    
    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {args[0]}")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), AgoraHandler) as httpd:
        print(f"🌐 Starting Agora server at http://localhost:{PORT}")
        print(f"📁 Using Agora APP_ID: {APP_ID}")
        print(f"📝 Using channel: {CHANNEL_NAME}")
        print(f"🔑 Token generated and will be injected into HTML")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            httpd.shutdown()