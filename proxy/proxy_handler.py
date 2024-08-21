import os
import subprocess
import requests
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/upload':
            file_path = self.headers.get('X-File-Name')
            logging.info(f'Received upload request for file: {file_path}')
            
            if file_path:
                scan_result = self.scan_file(file_path)
                status = 'clean' if scan_result else 'infected'
                logging.info(f'Scan result for {file_path}: {status}')
                
                if scan_result:
                    self.forward_file(file_path)
                    logging.info(f'Forwarded file {file_path} to main service.')
                
                self.send_result(file_path, status)
                
                if not scan_result:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logging.warning(f'Removed infected file: {file_path}')
                    else:
                        logging.error(f'File not found for removal: {file_path}')
            else:
                logging.error('No file name provided in the request headers.')
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'File name not provided')
        else:
            logging.info(f'Received: {self.path}')

    def scan_file(self, file_path):
        logging.info(f'Scanning file: {file_path}')
        result = subprocess.run(['clamscan', file_path], capture_output=True, text=True)
        logging.debug(f'Scan output: {result.stdout}')
        return 'Infected' not in result.stdout

    def forward_file(self, file_path):
        logging.info(f'Forwarding file: {file_path}')
        with open(file_path, 'rb') as f:
            response = requests.post('http://nginx-main:88/api/upload', files={'file': f})
            if response.status_code == 200:
                logging.info(f'Successfully forwarded file: {file_path}')
            else:
                logging.error(f'Failed to forward file: {file_path}, status code: {response.status_code}')

    def send_result(self, file_path, status):
        filename = os.path.basename(file_path)
        logging.info(f'Sending scan result for {filename}: {status}')
        
        response = requests.post('http://nginx-main:88/api/file_status', json={'filename': filename, 'status': status})
        if response.status_code in [200, 201]:
            logging.info(f'Successfully sent status for {filename}')
        else:
            logging.error(f'Failed to send status for {filename}, status code: {response.status_code}')

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'File processed')


logging.info('Starting HTTP server on port 8010...')
httpd = HTTPServer(('', 8010), ProxyHandler)
httpd.serve_forever()
