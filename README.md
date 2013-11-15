redis-router
============

<strong>redis_router</strong>, a redis sharding library/api for your redis sharding needs.

<img src="https://raw.github.com/emre/redis-router/master/workflow.png">

how it works
==============

<a href="http://en.wikipedia.org/wiki/Consistent_hashing">wikipedia/consistent_hashing</a>

> Consistent hashing is a special kind of hashing. When a hash table is resized and consistent hashing is used,
> only K/n keys need to be remapped on average, where K is the number of keys, and n is the number of slots.
> In contrast, in most traditional hash tables, a change in the number of array slots causes
> nearly all keys to be remapped.

redis_router uses <a href="http://last.fm">last.fm</a>'s <a href="https://github.com/RJ/ketama">
libketama</a> in the back.</li>

installation
==========

install <a href="https://github.com/RJ/ketama">libketama/ketama_python </a> first.

After that;

```
pip install redis-router
```
or if you like 90s:

```
easy_install redis-router
```

or add redis_router directory to the your path.


quick start
============


servers.txt (server:ip weight)
``` 
127.0.0.1:6379 100
127.0.0.1:6380 100
```

your python code:

``` python
router = Router("servers.txt")

router.set("forge", 13)
router.set("spawning_pool", 18)
```

output with loglevel=DEBUG

```
DEBUG:key 'forge' hashed as 4113771093 and mapped to 127.0.0.1:6379
DEBUG:key 'spawning_pool' hashed as 1434709819 and mapped to 127.0.0.1:6380
DEBUG:key 'forge' hashed as 4113771093 and mapped to 127.0.0.1:6379
DEBUG:key 'spawning_pool' hashed as 1434709819 and mapped to 127.0.0.1:6380
13 6
```

redis_router as a server
========================================
If you have clients using X programming language other than python, you can use HTTP or TCP interface to connect 
and send commands to redis_router.

running TCP interface
=======================

``` python
from redis_router.tcp_interface import RouterServer

r = RouterServer('0.0.0.0', 5000)
r.run()
```

<strong>playing with it</strong>
```
$ telnet localhost 5000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
set selam timu
True
get selam
timu
dbsize
13
```

HTTP API
=============

``` python
from redis_router.http_interface import start_server

start_server('0.0.0.0', 5000)
```

example request:

* initialize a set with two members.

``` bash
$ curl -X POST --data "command=sadd&arguments=teams,galatasaray,fenerbahce" http://localhost:5000 
```
``` json
{
  "response": 2
}
```
* get members

``` bash
$ curl -X POST --data "command=smembers&arguments=teams" http://localhost:5000
```

``` json
{
  "response": [
    "fenerbahce", 
    "galatasaray"
  ]
}
```

running tests
=================
``` bash
$ py.test tests.py 
=============================================== test session starts =========================
platform linux2 -- Python 2.7.3 -- pytest-2.3.4
collected 11 items 

tests.py ...........

============================================ 11 passed in 0.33 seconds ======================
```

FAQ
=========
 > Q: What about data invalidation if I move servers, change the config etc.

It's minimum. At least better than:
```
Node = Hash(key) MOD N
```

> Q: I want to see some stats about sharding efficiency.

Results for 100.000 random keys.
```
results: {
    redis.client.Redis object at 0x8df75a4: 33558,
    redis.client.Redis object at 0x8df7644: 31207,
    redis.client.Redis object at 0x8df7504: 35235
}
```
<img src="https://raw.github.com/emre/redis-router/master/shardacross.png">

> Q: Can I use this with PHP or [INSERT RANDOM LANGUAGE HERE]

Yes.

There are <a href="https://github.com/emre/redis-router/blob/master/redis_router/tcp_interface.py">TCP server</a> 
and <a href="https://github.com/emre/redis-router/blob/master/redis_router/http_interface.py">HTTP Server</a> options</a>. 
You can always use libketama's implementations in your language though.


 





[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/emre/redis-router/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

