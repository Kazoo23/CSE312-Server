from util.response import Response
class Router:

    def __init__(self):
        self.routes = []

    def add_route(self, method, path, action, exact_path=False):
        self.routes.append({
            'path': path,
            'method': method,
            'action': action,
            'exact_path': exact_path
        })

    def route_request(self, request, handler):
        for route in self.routes:
            if route["method"] == request.method:
                if route["exact_path"] and request.path == route["path"] or not route["exact_path"] and request.path.startswith(route["path"]):
                    route["action"](request, handler)
                    return
        res = Response()
        res.set_status("404", "Not Found")
        res.text("No route found")
        handler.request.sendall(res.to_data())
