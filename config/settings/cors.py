from corsheaders.defaults import default_headers

# If you want to allow all origins, use the following:
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  # Allow cookies to be sent with cross-origin requests
CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-Custom-Header",  # Add custom headers if needed
]
# Allow specific HTTP methods
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]
