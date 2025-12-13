"""
Gunicorn server configuration
"""
import multiprocessing
import os

# Server socket configuration
bind = ["0.0.0.0:8000"]
backlog = 2048

# Worker processes configuration
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeout configuration
timeout = 30
graceful_timeout = 30

# Server mechanics
daemon = False
pidfile = "/var/run/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging configuration
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = "mwecau_ict"

# SSL configuration (optional)
keyfile = None
certfile = None
cert_reqs = 0
ca_certs = None
ciphers = None

# Server hooks
def when_ready(server):
    """Called when server is ready to accept connections"""
    print("Gunicorn server is ready. Spawning workers")

def on_exit(server):
    """Called when server is shutting down"""
    print("Gunicorn server is shutting down")

def pre_fork(server, worker):
    """Called before forking worker"""
    pass

def post_fork(server, worker):
    """Called after forking worker"""
    pass

def pre_exec(server):
    """Called before executing server"""
    pass

def post_worker_int(worker):
    """Called after worker receives SIGINT"""
    pass

def worker_int(worker):
    """Called when worker receives SIGINT"""
    pass

def worker_abort(worker):
    """Called when worker is aborted"""
    pass

# Application configuration
raw_env = [
    "DJANGO_SETTINGS_MODULE=config.settings",
]

# Security
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190
