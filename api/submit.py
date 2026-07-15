from http.server import BaseHTTPRequestHandler
import json, urllib.request, os

AIRTABLE_TOKEN = os.environ.get("AIRTABLE_API_KEY", "")
AIRTABLE_URL = "https://api.airtable.com/v0/appNJD4UDbvCvkDkt/tblvYyRqFxQ20P0Q3"

def _cors(self):
    self.send_header("Access-Control-Allow-Origin", "*")
    self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    self.send_header("Access-Control-Allow-Headers", "Content-Type")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_len))
        except Exception:
            self.send_response(400)
            _cors(self)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": "invalid json"}).encode())
            return

        req = urllib.request.Request(
            AIRTABLE_URL,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {AIRTABLE_TOKEN}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read())
            self.send_response(200)
            _cors(self)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "count": len(result.get("records", []))}).encode())
        except urllib.request.HTTPError as e:
            self.send_response(e.code)
            _cors(self)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": f"airtable error {e.code}"}).encode())
        except Exception as e:
            self.send_response(500)
            _cors(self)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        _cors(self)
        self.end_headers()
