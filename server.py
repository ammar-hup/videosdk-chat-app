#!/usr/bin/env python3
"""
Simple HTTP server to serve the VideoSDK web interface
Enhanced for ngrok compatibility
"""

import http.server
import socketserver
import os
import webbrowser
from threading import Timer
import socket
import urllib.request
import json

PORT = 8000
DIRECTORY = os.path.join(os.path.dirname(__file__), "web")

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
        
    def end_headers(self):
        # Add CORS headers for ngrok compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
        
    def do_OPTIONS(self):
        # Handle preflight requests for CORS
        self.send_response(200)
        self.end_headers()
        
    def log_message(self, format, *args):
        # Add IP address info to distinguish clients
        super().log_message(format + " - %s", *args, self.client_address[0])

def open_browser():
    """Open browser after a short delay"""
    webbrowser.open(f'http://localhost:{PORT}')

def get_ngrok_url():
    """Try to get the public ngrok URL if it's running"""
    try:
        response = urllib.request.urlopen('http://localhost:4040/api/tunnels')
        data = json.loads(response.read().decode())
        return data['tunnels'][0]['public_url']
    except:
        return None

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    
    # Allow the socket to be reused immediately after the server is stopped
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", PORT), CORSHandler) as httpd:
        local_url = f"http://localhost:{PORT}"
        print(f"🌐 Starting server at {local_url}")
        print(f"📁 Serving files from: {DIRECTORY}")
        
        # Check if ngrok is running and display the public URL
        ngrok_url = get_ngrok_url()
        if ngrok_url:
            print(f"🚀 Ngrok tunnel active: {ngrok_url}")
            print(f"✅ Your application is publicly accessible!")
        else:
            print(f"🎥 Open {local_url} in your browser to test the video chat")
            print("💡 TIP: Run ngrok in another terminal with 'ngrok http 8000' for public access")
        
        print("Press Ctrl+C to stop the server")
        
        # Auto-open browser after 1 second
        Timer(1.0, open_browser).start()
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
