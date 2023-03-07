import redis
import time
import sys

def producer():
    r = redis.Redis(host='docker.for.linux.localhost')

    i = 0
    while True:
        r.publish('queue', 'Message %d' % i)
        i += 1
        time.sleep(1)

def consumer():
    r = redis.Redis(host='0.0.0.0')
    while True:
        # val = r.blpop('queue')
        sub = r.pubsub()
        sub.subscribe('queue')
        for message in sub.listen():
            if message is not None:
                print(f'Consuming: {message}')

if __name__ == '__main__':
    """
    Open up two terminals and run the two commands separately
    """
    consumer()
    # if sys.argv[1] == 'consumer':
    #     print("Starting consumer: ")
    #     consumer()
    # else:
    #     print("Starting producer: ")
    #     producer()