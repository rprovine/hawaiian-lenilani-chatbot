#!/usr/bin/env python3
"""Simple HTTP server to test the widget locally"""
import http.server
import socketserver
import os

PORT = 8080

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"🌺 Widget demo server running at http://localhost:{PORT}")
    print(f"📖 Open http://localhost:{PORT}/widget-standalone.html")
    print("🤙 Press Ctrl+C to stop")
    httpd.serve_forever()