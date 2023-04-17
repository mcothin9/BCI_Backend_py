# server.py
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs
from test_result_server import predict_eeg_events

class MyRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/probs':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            probs = predict_eeg_events()
            probs_list = probs.tolist()
            response = {'probs': probs_list}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_error(404, 'Not Found')

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 5000), MyRequestHandler)
    print("Starting server on http://localhost:5000")
    server.serve_forever()
