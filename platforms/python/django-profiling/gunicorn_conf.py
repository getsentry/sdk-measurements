import multiprocessing
import os
import sys

_is_pypy = hasattr(sys, 'pypy_version_info')
_is_travis = os.environ.get('TRAVIS') == 'true'
_bind_port = os.environ.get('SENTRY_PORT_BACKEND', 8080)

workers = multiprocessing.cpu_count() * 3
if _is_travis:
    workers = 2

bind = "0.0.0.0:{}".format(_bind_port)
keepalive = 120
errorlog = '-'
pidfile = 'gunicorn.pid'
pythonpath = 'hello'

if _is_pypy:
    worker_class = "tornado"
else:
    worker_class = "meinheld.gmeinheld.MeinheldWorker"

    def post_fork(server, worker):
        # Disalbe access log
        import meinheld.server
        meinheld.server.set_access_logger(None)
