__author__ = 'MilanAshara'

# class Singleton(object):
#   _instances = {}
#   _cache= "test"
#   def __new__(class_, *args, **kwargs):
#     if class_ not in class_._instances:
#         class_._instances[class_] = super(Singleton, class_).__new__(class_, *args, **kwargs)
#     return class_._instances[class_]._cache
#
# class MyClass(Singleton):
#   pass
#
# print  Singleton()
# print Singleton.cache
import threading
# class SovCache(object):
#     _cache = None
#     is_auto_refresh_started = False
#
#     def __new__(cls):  # __new__ always a classmethod
#         if not SovCache._cache and not SovCache.is_auto_refresh_started:
#             SovCache.is_auto_refresh_started = True
#             SovCache._cache = cache_sov_for_prev_two_dates()
#             threading.Timer(0, update_sov_cache).start()
#         return SovCache._cache
#
#
# def cache_sov_for_prev_two_dates(key="milan"):
#     print "cache_sov_for_prev_two_dates"
#     SovCache._cache=key
#     return key
#
# def update_sov_cache():
#     """
#     This method updates sov cache every TIME_TO_LIVE_SOV_CACHE_SECONDS
#     :return: None
#     """
#     cache_sov_for_prev_two_dates(key="asddas")
#     threading.Timer(3, update_sov_cache).start()
#
# print SovCache()
# threading._sleep(10)
# print SovCache()
# print SovCache()
# print SovCache()
# print SovCache()
# print SovCache()


class Test(object):
    instance=None

print Test.instance
Test.instance=464
print Test.instance