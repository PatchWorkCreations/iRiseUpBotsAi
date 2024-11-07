# myapp/middleware.py
import os
from django.http import HttpResponseRedirect
from django.conf import settings

class MissingStaticFileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for a static file
        if request.path.startswith(settings.STATIC_URL):
            # Get the absolute path to the static file
            static_path = os.path.join(settings.STATIC_ROOT, request.path[len(settings.STATIC_URL):])
            # Check if the file exists in STATIC_ROOT
            if not os.path.exists(static_path):
                # Redirect to a default fallback image
                return HttpResponseRedirect(settings.STATIC_URL + 'myapp/images/iriseuplogo.svg')
        # Proceed with the normal response if no issue
        return self.get_response(request)
    
