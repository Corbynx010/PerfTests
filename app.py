import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379, db=0)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


def store_prime(x):
    retries = 5
    while True:
        try:
            cache.lrem('primeList',0,x)
            return cache.lpush('primeList',x)
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_primes():
    retries = 5
    primes = ''
    while True:
        try:
            for i in range(0, cache.llen('primeList')):
                primes = primes + str(cache.lindex('primeList',i))[2:-1] + '\n'
            return primes
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)

@app.route('/isPrime/<x>')
def isPrime(x):
    n=float(x)
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return str(x) + ' is not a prime number.\n'

    store_prime(x)
    return str(x) + ' is a prime number.\n'

@app.route('/primesStored')
def primesStored():
    return get_primes()
    
