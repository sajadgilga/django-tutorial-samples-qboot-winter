import json
from http.server import HTTPServer, BaseHTTPRequestHandler


class Profile:
    name: str
    age: int

    def __init__(self, name, age):
        self.name = name
        self.age = age


class ProfileEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Profile):
            return obj.__dict__
        return super().default(obj)


profile = Profile(None, None)


class MyHandler(BaseHTTPRequestHandler):
    def _send_response(self, data, status, encoder=None):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data, cls=encoder).encode('utf-8'))

    def do_GET(self):
        if self.path == '/hello':
            data = {'message': 'Hello World'}
            self._send_response(data, 200)
        elif self.path == '/profile':
            data = profile
            self._send_response(data, 200, encoder=ProfileEncoder)
        else:
            self._send_response({'message': 'Not Found'}, 404)

    def do_PUT(self):
        if self.path == '/profile':
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            print(f'Request body before json load: {request_body}')
            request_body = json.loads(request_body)
            print(f'Request body before json load: {request_body}')
            global profile
            profile.name = request_body['name']
            self._send_response({'message': 'success'}, 201)


server = HTTPServer(('', 8000), MyHandler)

print('server setup done, ready to serve...')
server.serve_forever()
