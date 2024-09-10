from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

class WebRequestHandler(BaseHTTPRequestHandler):
    CONTENTS = {
        '/': "<html><h1>Home Page</h1></html>",
        '/proyecto/web-uno': "<html><h1>Proyecto: web-uno</h1></html>",
        '/proyecto/web-dos': "<html><h1>Proyecto: web-dos</h1></html>",
        '/proyecto/web-tres': "<html><h1>Proyecto: web-tres</h1></html>",
    }

    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):
        # REGISTRO DE LA PETICION "GET"
        host_header = self.headers.get('Host')
        user_agent_header = self.headers.get('User-Agent')
        requested_path = self.path

        # GENERAR UN RESPUESTA EN HTML, BASANDOSE EN EL CONTENIDO EN MEMORIA
        response_message = self.get_response()

        # ENVIA LA RESPUESTA
        status_code = 200 if self.path in self.CONTENTS else 404
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.send_header("Server", "Python HTTP Server")
        self.send_header("Date", self.date_time_string())
        self.end_headers()
        self.wfile.write(response_message.encode("utf-8"))

        # IMPRIME LA INFORMACION EN LA CONSOLA
        print(f"Request:")
        print(f"  Host: {host_header}")
        print(f"  User-Agent: {user_agent_header}")
        print(f"  Requested Path: {requested_path}")
        print(f"Response:")
        print(f"  Content-Type: text/html")
        print(f"  Server: Python HTTP Server")
        print(f"  Date: {self.date_time_string()}")

    def do_POST(self):
        # RESPUESTA DE LA PETICION "POST"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.send_header("Server", "Python HTTP Server")
        self.send_header("Date", self.date_time_string())
        self.end_headers()
        self.wfile.write(b"POST request received!")

    def get_response(self):
        # RESPUESTA CON EL CONTENIDO HTML DESDE EL DICCIONARIO 
        return self.CONTENTS.get(self.path, "<h1>Error 404: Not Found</h1>")

if _name_ == "_main_":
    print("Starting server on port 8000")
    server = HTTPServer(("localhost", 8000), WebRequestHandler)
    server.serve_forever()
