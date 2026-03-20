import http.server
import socketserver
import ssl
import argparse
import os

class BrotliRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        if self.path.endswith(".br"):
            self.send_header("Content-Encoding", "br")
        super().end_headers()

    def guess_type(self, path):
        if path.endswith(".js.br"):
            return "application/javascript"
        if path.endswith(".wasm.br"):
            return "application/wasm"
        return super().guess_type(path)

def run_server():
    parser = argparse.ArgumentParser(description="Brotli-enabled HTTPS Server")
    parser.add_argument("--dir", default=".", help="Directory to serve")
    parser.add_argument("--localhost", action="store_true", help="Bind to localhost (default: False)")
    parser.add_argument("--port", type=int, default=4443, help="Port (default: 4443)")
    parser.add_argument("--cert", default="cert.pem", help="Path to certificate .pem file")
    parser.add_argument("--key", default="key.pem", help="Path to key .pem file")
    args = parser.parse_args()

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=args.cert, keyfile=args.key)

    handler = lambda *a, **k: BrotliRequestHandler(*a, directory=args.dir, **k)

    bind_url = "localhost" if args.localhost else "0.0.0.0"
    with socketserver.TCPServer((bind_url, args.port), handler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        print(f"Serving HTTPS at https://{bind_url}:{args.port}")
        print(f"Directory: {os.path.abspath(args.dir)}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down.")

if __name__ == "__main__":
    run_server()
