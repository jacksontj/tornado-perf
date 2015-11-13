import time
import sys

import tornado.gen
import tornado.ioloop
import tornado.httpclient

total_requests = 0
total_success = 0

URL = 'http://10.0.1.10/test'


@tornado.gen.coroutine
def fetch(client):
    global total_requests
    global total_success

    total_requests += 1
    ret = yield client.fetch(
        URL,
        request_timeout=1,
    )
    if ret.code == 200:
        total_success += 1


@tornado.gen.coroutine
def main():
    http_client = tornado.httpclient.AsyncHTTPClient(
        max_clients=200,
        #hostname_mapping={'10.0.1.10': '10.0.1.10'},
    )
    while True:
        fetch(http_client)
        yield tornado.gen.moment


last_requests = last_success = 0
def callcount():
    global total_requests
    global total_success

    global last_requests
    global last_success


    print ('Metrics: req:{req}, success: {suc}, queue:{q}'.format(
        req=total_requests - last_requests,
        suc=total_success - last_success,
        q=total_requests - total_success,
    ))
    last_requests = total_requests
    last_success = total_success

    tornado.ioloop.IOLoop.current().add_timeout(time.time() + 1, callcount)


last = time.time()
def pacemaker():
    global last
    now = time.time()
    print ('Pacemaker: {0}'.format(now - last - 1))
    last = now

    tornado.ioloop.IOLoop.current().add_timeout(time.time() + 1, pacemaker)



if __name__ == '__main__':

    loop = tornado.ioloop.IOLoop.current()
    if len(sys.argv) == 2:
        URL = sys.argv[1]

    tornado.httpclient.AsyncHTTPClient.configure("tornado.simple_httpclient.SimpleAsyncHTTPClient")

    # add caller to do requests
    loop.add_callback(main)

    # add printer of QPS
    loop.add_callback(callcount)

    # add pacemaker
    loop.add_callback(pacemaker)

    loop.start()
