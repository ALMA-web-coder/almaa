import threading

# Thread-local storage to store per-request data
_thread_locals = threading.local()

def get_current_user():
    return getattr(_thread_locals, 'user', None)

class CurrentUserMiddleware:
    """
    Middleware to store the current user in thread-local storage.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Store the user for the duration of the request
        _thread_locals.user = getattr(request, 'user', None)
        response = self.get_response(request)
        # Clear user after response to avoid leaks in long-running threads
        _thread_locals.user = None
        return response