import os
import redis
from rq import Connection, Queue, Worker
from url_shortener import create_app

redis_url = os.environ.get('REDISTOGO_URL') or 'redis://localhost:6379'

conn = redis.from_url(redis_url)
try:
    conn.ping()
except redis.ConnectionError as err:
    import sys
    sys.exit(0)


app = create_app(os.environ.get('FLAsK_CONFIG') or 'default')
app.app_context().push()

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(['default'], connection=conn, name='db_cleaner')
        worker.work()
