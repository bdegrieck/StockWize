from datetime import datetime, timedelta

class CacheDependency:
    """
    A class to handle caching of function calls with a specified time-to-live (TTL).

    ### Attributes:
    time_to_live (int): The time-to-live for cache entries in days. Defaults to 1 day.

    ### Methods:
    call(call, cache_key): Calls the provided function and caches its result using the specified cache key.
    The cache key will typically be a string that uniquely identifies this API call, such as
    the API being called + input parameters.

    ### Example usage:
    ```
    def some_slow_api_call(input):
        # Make call to slow API, return results

    cache = CacheDependency(time_to_live=1)
    input = "some value"
    value = cache.call(lambda : some_slow_api_call(input), input)
    ```
    """

    def __init__(self, time_to_live=1):
        self._cache = {}
        self.time_to_live = time_to_live
    
    def call(self, call, cache_key):
        if cache_key in self._cache:
            if datetime.now() - self._cache[cache_key]['time'] < timedelta(days=self.time_to_live):
                return self._cache[cache_key]['value']
            else:
                del self._cache[cache_key]

        value = call()
        self._cache[cache_key] = {'value': value, 'time': datetime.now()}
        return value