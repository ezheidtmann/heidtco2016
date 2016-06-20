import redis_lock
from django.conf import settings

def get_client():
    from django.core.cache import caches
    cache = caches[settings.REDIS_LOCKING_CACHE_KEY]
    try:
        return cache.clients.items()[0][1]
    except AttributeError:
        return cache.client

def get_lock(name, **kwargs):
    return redis_lock.Lock(get_client(), name, **kwargs)
