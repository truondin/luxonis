from http.server import SimpleHTTPRequestHandler, HTTPServer
from jinja2 import Template
import psycopg2


class SrealityHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('index.html', 'r') as file:
                template_content = file.read()
            template = Template(template_content)

            data = get_data_from_database()
            html_content = template.render(items=data)

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))

        else:
            super().do_GET()


def get_data_from_database():
    conn = psycopg2.connect(
            dbname="sreality",
            user="postgres",
            password="password",
            host="postgres",
            port="5432"
        )
    cursor = conn.cursor()

    cursor.execute("SELECT title, img_url FROM properties")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    items_list = []
    for title, img_url in data:
        items_list.append({'title': title, 'img_url': img_url})
    return items_list


def run(server_class=HTTPServer, handler_class=SrealityHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
