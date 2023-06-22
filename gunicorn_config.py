#!/usr/bin/python3

# Number of worker processes
workers = 4

# The type of worker processes to use
worker_class = 'gevent'

# The host and port to bind to
bind = '0.0.0.0:5000'

# The maximum number of requests a worker will process before restarting
max_requests = 1000

# The maximum number of seconds a worker will live
max_requests_jitter = 100

# The log level
loglevel = 'info'

# Path to the Flask application
app_module = 'api.v1.app:app'
