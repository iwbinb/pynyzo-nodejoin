from redis import Redis
from rq import Queue, Worker
worker = Worker(Queue('ipflow'), connection=Redis())
