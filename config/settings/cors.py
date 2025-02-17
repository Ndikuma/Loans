from corsheaders.defaults import default_headers

# If you want to allow all origins, use the following:
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  # Allow cookies to be sent with cross-origin requests
CORS_ALLOW_HEADERS = list(default_headers) + [
    "X-Custom-Header",  # Add custom headers if needed
    "Authorization",  # If using JWT tokens
    "Content-Type",
    "X-Requested-With",  # If using X-Requested-With header
    "X-CSRFToken",  # If using CSRF protection
    "Accept",
    "Origin",
    "Referer",
    "User-Agent",
    "X-Custom-Header",  # Add custom headers if needed
    "Accept-Encoding",
    "Accept-Language",

]
# Allow specific HTTP methods
CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
    "HEAD",
    "TRACE",
    "CONNECT",
    "PURGE",
    "LINK",
    "UNLINK",
]
