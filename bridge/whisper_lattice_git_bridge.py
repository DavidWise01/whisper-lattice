#!/usr/bin/env python3
# whisper_lattice_git_bridge.py
# Local git control plane for Whisper Lattice
# Receives POSTs from browser and commits to local git repo

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import subprocess

REPO_PATH = os.path.expanduser("~/whisper-lattice-log")
LOG_FILE = os.path.join(REPO_PATH, "lattice_events.jsonl")
MARKDOWN_FILE = os.path.join(REPO_PATH, "UNITY_LOG.md")

os.makedirs(REPO_PATH, exist_ok=True)

# init git repo if needed
if not os.path.exists(os.path.join(REPO_PATH, ".git")):
    subprocess.run(["git", "init"], cwd=REPO_PATH, capture_output=True)
    with open(os.path.join(REPO_PATH, ".gitignore"), "w") as f:
        f.write("__pycache__/\n*.pyc\n")
    subprocess.run(["git", "add", "."], cwd=REPO_PATH, capture_output=True)
    subprocess.run(["git", "commit", "-m", "init whisper lattice log"], cwd=REPO_PATH, capture_output=True)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        try:
            event = json.loads(data)
        except:
            event = {"raw": data.decode('utf-8', errors='ignore')}
        
        # append to jsonl
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        # append to markdown
        ts = event.get("timestamp", datetime.utcnow().isoformat())
        depth = event.get("depth", "?")
        coh = event.get("coherence", "?")
        ev = event.get("event", "update")
        
        with open(MARKDOWN_FILE, "a") as f:
            f.write(f"\n## {ts} — {ev}\n")
            f.write(f"- **Depth:** {depth}\n")
            f.write(f"- **Coherence:** {coh}\n")
            f.write(f"- **Recursive:** {event.get('recursive_coherence', '?')}\n")
            f.write(f"- **Observers:** {event.get('observers_active', 5)}/5\n")
            f.write(f"- **Tether:** {event.get('tether_state', 'unknown')}\n")
            f.write(f"```json\n{json.dumps(event, indent=2)}\n```\n")
        
        # git commit
        try:
            subprocess.run(["git", "add", "."], cwd=REPO_PATH, capture_output=True)
            msg = f"lattice: {ev} depth {depth} coh {coh}"
            subprocess.run(["git", "commit", "-m", msg], cwd=REPO_PATH, capture_output=True)
        except Exception as e:
            print("git error:", e)
        
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"logged"}')
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    port = 8787
    print(f"Whisper Lattice Git Bridge running on http://localhost:{port}")
    print(f"Repo: {REPO_PATH}")
    print("Set your Central Bridge URL to: http://localhost:8787")
    print("Ctrl+C to stop")
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
