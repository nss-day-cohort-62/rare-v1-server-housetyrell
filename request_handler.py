from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from views import get_all_categories, create_category, get_all_comments, get_all_post_reactions, get_all_posts, get_single_posts, get_all_reactions, get_all_subscriptions, create_subscription, get_all_tags, login_user, create_user, get_all_users, get_single_user, get_all_post_tags, get_post_by_search
from views import get_single_comment, create_comment, get_single_tag, create_post, update_post, delete_post, create_tag, create_post_tag, create_subscription, delete_comment, delete_subscription


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != '':
            query_params = parse_qs(url_components.query)
         
        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

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
        self._set_headers(200)
        response = None
        parsed = self.parse_url(self.path)
        if '?' not in self.path:
            (resource, id, query_params) = parsed
            if resource == "posts":
                if id is not None:
                    response = get_single_posts(id)
                else:
                    response = get_all_posts(query_params)
            if resource == "categories":
                response = get_all_categories()
            if resource == "comments":
                if id is not None:
                    response = get_single_comment(id)
                else:
                    response = get_all_comments()
            if resource == "post_reactions":
                response = get_all_post_reactions()
            if resource == "post_tags":
                response = get_all_post_tags()
            if resource == "users":
                if id is not None:
                    response = get_single_user(id)
                else:
                    response = get_all_users()
            if resource == "subscriptions":
                response = get_all_subscriptions(query_params)
            if resource == "reactions":
                response = get_all_reactions()
            if resource == "tags":
                if id is not None:
                    response = get_single_tag(id)
                else:
                    response = get_all_tags()
        else:
            (resource, id, query_params) = parsed
            # print(query_params)
            if resource == "posts":
                if query_params.get('search'):
                    response = get_post_by_search(query_params['search'][0])
                else:
                    response = get_all_posts(query_params)
            if resource == "subscriptions":
                response = get_all_subscriptions(query_params)
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)
        # Parse the URL
        (resource, id, query_params) = self.parse_url(self.path)

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'posts':
            response = create_post(post_body)
        if resource == 'comments':
            response = create_comment(post_body)
        if resource == 'categories':
            response = create_category(post_body)
        if resource == 'tags':
            response = create_tag(post_body)
        if resource == 'posttags':
            response = create_post_tag(post_body)
        if resource == 'subscriptions':
            response = create_subscription(post_body)

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        resource, id, query_params = self.parse_url(self.path)
        success = False
        if resource == "posts":
            success = update_post(id, post_body)
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        #self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)
        resource, id, query_params = self.parse_url(self.path)

        if resource == "posts":
            delete_post(id)
        if resource == "comments":
            delete_comment(id)
        if resource == "subscriptions":
            delete_subscription(id)


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
