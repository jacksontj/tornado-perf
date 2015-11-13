import aiohttp
import asyncio
import time

URL = 'http://10.0.1.10/test'

total_requests = 0
total_success = 0

@asyncio.coroutine
def get_body(client, url):
    global total_requests
    global total_success

    total_requests += 1

    response = yield from client.head(url)
    if response.status == 200:
        total_success += 1
    yield from response.read()


last_requests = last_success = 0
@asyncio.coroutine
def callcount():
    global total_requests
    global total_success

    global last_requests
    global last_success

    while True:
        print ('Metrics: req:{req}, success: {suc}, queue:{q}'.format(
            req=total_requests - last_requests,
            suc=total_success - last_success,
            q=total_requests - total_success,
        ))
        last_requests = total_requests
        last_success = total_success

        yield from asyncio.sleep(1)


last = time.time()
@asyncio.coroutine
def pacemaker():
    global last
    while True:
        now = time.time()
        print ('Pacemaker: {0}'.format(now - last - 1))
        last = now

        yield from asyncio.sleep(1)


@asyncio.coroutine
def main():
    print ('here')
    loop = asyncio.get_event_loop()
    print (loop)
    client = aiohttp.ClientSession()
    i = 0
    while True:
        loop.create_task(get_body(client, URL))
        i += 1
        yield from asyncio.sleep(0)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.create_task(callcount())
    loop.create_task(pacemaker())

    print (loop)

    loop.run_forever()
