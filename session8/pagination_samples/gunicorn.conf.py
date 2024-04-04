workers = 8
worker_class = 'gthread'
threads = 10
timeout = 10
bind = "127.0.0.1:8000"
keepalive = 3
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"
max_requests = 100
max_requests_jitter = 20


def when_ready(server):
    print('app is ready')


def pre_fork(server, worker):
    print('before worker forking')


def post_fork(server, worker):
    print('after worker forking')


def pre_request(worker, req):
    print('before request processing')
