# Enable Silk
SILKY_PYTHON_PROFILER = True  # Enable Python code profiling
SILKY_PYTHON_PROFILER_BINARY = (
    False  # Set to True if you want binary data for profiling
)

# Control SQL query analysis
SILKY_ANALYZE_QUERIES = True  # Analyze database queries

# Database table trimming (to prevent Silk from storing excessive data)
SILKY_MAX_REQUEST_BODY_SIZE = -1  # Default: -1 (no limit)
SILKY_MAX_RESPONSE_BODY_SIZE = 1024  # Default: 1024 bytes
