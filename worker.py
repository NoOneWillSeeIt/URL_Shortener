import os
import redis
from datetime import timedelta
from rq import Queue
from rq_scheduler import Scheduler
from url_shortener.utils import delete_overdue_links

redis_url = os.environ.get('REDISTOGO_URL') or 'redis://localhost:6379'

conn = redis.from_url(redis_url)

scheduler = Scheduler(connection=conn)

scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=delete_overdue_links,
    interval=timedelta(hours=48).total_seconds(),
    repeat=None
    )