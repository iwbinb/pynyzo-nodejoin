from redis import Redis
from rq import Queue, Worker

redis = Redis()
queue = Queue('ipflow')

worker = Worker([queue], connection=redis)
