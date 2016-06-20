from redis_lock import Lock
from redis_lock.django_cache import RedisCache

class MyRedisCache(RedisCache):

    def lock(self, key, **kwargs):
        kwargs.setdefault('expire', 10)
        kwargs.setdefault('auto_renewal', True)
        return Lock(self._RedisCache__client, key, **kwargs)
