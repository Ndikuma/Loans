# Session Engine
SESSION_ENGINE = (
    "django.contrib.sessions.backends.db"  # Use the database to store session data
)

# Other options for SESSION_ENGINE:
# 'django.contrib.sessions.backends.cache'          # Use the cache
# 'django.contrib.sessions.backends.cached_db'      # Use both the database and cache
# 'django.contrib.sessions.backends.file'           # Use the filesystem
# 'django.contrib.sessions.backends.signed_cookies' # Store session data in cookies

# Session Cookie Name
SESSION_COOKIE_NAME = "sessionid"  # Default: 'sessionid'

# Session Cookie Age
SESSION_COOKIE_AGE = 1209600  # Two weeks in seconds (default)

# Session Cookie Secure
SESSION_COOKIE_SECURE = False  # Use True for HTTPS connections in production

# HTTP Only
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript from accessing the session cookie

# Path for the Cookie
SESSION_COOKIE_PATH = "/"  # Path where the session cookie is valid

# Session Cookie Domain
SESSION_COOKIE_DOMAIN = None  # Use this to set the domain for the session cookie

# Session Expiry
SESSION_EXPIRE_AT_BROWSER_CLOSE = (
    False  # Keep the session active after the browser is closed
)
SESSION_SAVE_EVERY_REQUEST = False  # Save the session on every request
