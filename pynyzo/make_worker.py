from redis import Redis
from rq import Queue, Worker

q = Queue('ipflow', connection=Redis())

worker = Worker([q])
