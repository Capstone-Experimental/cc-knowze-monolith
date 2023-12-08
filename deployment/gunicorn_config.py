import multiprocessing

bind = '0.0.0.0:8080'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gthread'
threads = 2 * multiprocessing.cpu_count()
timeout = 240
keepalive = 5