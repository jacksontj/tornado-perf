import time
import sys

import requests
import threading

total_requests = 0
total_success = 0

MAX_WORKERS = 200
URL = 'http://10.0.1.10/test'

stop = threading.Event()

def do_requests():
    global total_requests
    global total_success
    while not stop.is_set():
        ret = requests.get(URL)
        total_requests += 1
        if ret.status_code == 200:
            total_success += 1

last_requests = last_success = 0
def callcount():
    global total_requests
    global total_success

    global last_requests
    global last_success


    while not stop.is_set():
        print ('Metrics: req:{req}, success: {suc}, queue:{q}'.format(
            req=total_requests - last_requests,
            suc=total_success - last_success,
            q=total_requests - total_success,
        ))
        last_requests = total_requests
        last_success = total_success

        time.sleep(1)




if __name__ == '__main__':

    if len(sys.argv) == 2:
        URL = sys.argv[1]

    metrics = threading.Thread(target=callcount)
    metrics.daemon = True
    metrics.start()

    workers = []
    for x in xrange(0, MAX_WORKERS):
        t = threading.Thread(target=do_requests)
        t.daemon = True
        t.start()
        workers.append(t)

    try:
        print 'everything started'
        time.sleep(300)
    except:
        print 'stopping'
        stop.set()

    metrics.join()
    for w in workers:
        w.join()
