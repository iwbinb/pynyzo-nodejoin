import sys
from rq import Connection, Worker

with Connection():
    qs = sys.argv[1:] or ['ipflow']

    w = Worker(qs)
    w.work()
