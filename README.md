redis-router
============

<strong>redis_router</strong>, a redis sharding library/api for your redis sharding needs.

how it works
==============

<a href="http://en.wikipedia.org/wiki/Consistent_hashing">wikipedia/consistent_hashing</a>

> Consistent hashing is a special kind of hashing. 
> When a hash table is resized and consistent hashing is used, only  keys need to be remapped on average,
> where  is the number of keys, and  is the number of slots. In contrast, in most traditional hash tables,
> a change in the number of array slots causes nearly all keys to be remapped.

redis_router uses <a href="http://last.fm">last.fm</a>'s <a href="https://github.com/RJ/ketama">
libketama</a> in the back.</li>

installation
==========

```
pip install redis_router
```
or if you like 90s:

```
easy_install redis_router
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

> Q: Can I use this with PHP or [INSERT RANDOM LANGUAGE HERE]

Yes.

There is a <a href="https://github.com/emre/redis-router/blob/master/redis_router/tcp_interface.py">TCP server option</a>. You can always use libketama's implementations in your language though.


<img src="https://raw.github.com/emre/redis-router/master/shardacross.png">
 



