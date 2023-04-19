from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from views import get_all_categories, create_category, get_all_comments, get_all_post_reactions, get_all_posts, get_single_posts, get_all_reactions, get_all_subscriptions, get_all_tags, login_user, create_user, get_all_users, get_all_post_tags, create_post, update_post, delete_post, create_tag


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != '':
            query_params = url_components.query.split("&")

        resource = path_params[0]
        id = None
        try:
            id = int(path_params[1])
        except IndexError:
            pass 
        except ValueError:
            pass 

        return (resource, id, query_params)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        response = None
        parsed = self.parse_url(self.path)
        ( resource, id, query_params ) = parsed
        # if '?'  not in self.path:
        self._set_headers(200)
        if resource == "posts":
            if id is not None:
                response = get_single_posts(id)
            else:
                response = get_all_posts(query_params)
        if resource == "categories":
            response = get_all_categories()
        if resource == "comments":
            response = get_all_comments()
        if resource == "post_reactions":
            response = get_all_post_reactions()
        if resource == "post_tags":
            response = get_all_post_tags()
        if resource == "users":
            response = get_all_users()
        if resource == "subscriptions":
            response = get_all_subscriptions()
        if resource == "reactions":
            response = get_all_reactions()
        if resource == "tags":
            response = get_all_tags()

        self.wfile.write(json.dumps(response).encode())



    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _  = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'posts':
            response = create_post(post_body)
        if resource == 'categories':
            response = create_category(post_body)
        if resource == 'tags':
            response = create_tag(post_body)

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        resource, id = self.parse_url()
        success = False
        if resource == "posts":
            update_post(id, post_body)
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)
        resource, id = self.parse_url()

        if resource == "posts":
            delete_post(id)


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
