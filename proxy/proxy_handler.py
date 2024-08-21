import os
import subprocess
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

class ProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/upload':
            file_path = self.headers.get('X-File-Name')
            if file_path:
                scan_result = self.scan_file(file_path)
                # Определяем статус файла
                status = 'clean' if scan_result else 'infected'
                
                if scan_result:
                    self.forward_file(file_path)
                
                # Отправляем результат сканирования
                self.send_result(file_path, status)
                
                if not scan_result:
                    os.remove(file_path)

    def scan_file(self, file_path):
        result = subprocess.run(['clamscan', file_path], capture_output=True, text=True)
        return 'Infected' not in result.stdout

    def forward_file(self, file_path):
        with open(file_path, 'rb') as f:
            requests.post('http://main-container/api/upload', files={'file': f})

    def send_result(self, file_path, status):
        filename = os.path.basename(file_path)
        
        requests.post('http://main-container/api/file_status', json={'filename': filename, 'status': status})

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File processed')

httpd = HTTPServer(('', 8000), ProxyHandler)
httpd.serve_forever()