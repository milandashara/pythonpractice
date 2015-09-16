__author__ = 'xxmajia'


"""
Warning: should never refer to this file directly, should always use couchbase_wrapper as a facade
This file holds a couchbase connection pool, we don't close tcp connection explicitly, instead, we keep it
"""
from couchbase.bucket import Bucket
from Queue import Queue, Empty
from threading import Lock
from time import time
import logging


logger = logging.getLogger('travelrankings')


class ClientUnavailableError(Exception):
    pass


class BucketWrapper(Bucket):
    """
    This is a simple subclass which adds usage statistics to inspect later on
    TODO: should implement init close method to use keyword with other than try-finally
    """
    def __init__(self, **kwargs):
        super(BucketWrapper, self).__init__(**kwargs)
        self.use_count = 0
        self.use_time = 0
        self.last_use_time = 0

    def start_using(self):
        self.last_use_time = time()

    def stop_using(self):
        self.use_time += time() - self.last_use_time
        self.use_count += 1

    def get_status(self):
        return 'use count: %s, use time: %s, last use time: %s' % (self.use_count, self.use_time, self.last_use_time)


class Pool(object):
    def __init__(self, initial=2, max_clients=10, **connargs):
        """
        Create a new pool
        :param int initial: The initial number of client objects to create
        :param int max_clients: The maximum amount of clients to create. These
          clients will only be created on demand and will potentially be
          destroyed once they have been returned via a call to
          :meth:`release_client`
        :param connargs: Extra arguments to pass to the Connection object's
        constructor
        """
        self._q = Queue()
        self._l = []
        self._connargs = connargs
        self._cur_clients = 0
        self._max_clients = max_clients
        self._lock = Lock()

        for x in range(initial):
            self._q.put(self._make_client())

    def get_max_size(self):
        return self._max_clients

    def get_actual_size(self):
        return self._cur_clients

    def get_pool_status(self):
        return {
            'max_size': self.get_max_size(),
            'actual_size': self.get_actual_size()
        }

    def _make_client(self):
        ret = BucketWrapper(**self._connargs)
        self._l.append(ret)
        self._cur_clients += 1
        logger.info('Launch a new couchbase client, # of clients: %s' % self._cur_clients)
        return ret

    def get_client(self, initial_timeout=0.5, next_timeout=5):
        """
        Should not called this method externally unless you need some special feature,
        because you need to release the client,
        should call get_resultset_from_view for view usage
        or call get_multi for key-value usage

        Wait until a client instance is available
        both initial_timeout and next_timeout are in second
        :param float initial_timeout:
          how long to wait initially for an existing client to complete
        :param float next_timeout:
          if the pool could not obtain a client during the initial timeout,
          and we have allocated the maximum available number of clients, wait
          this long until we can retrieve another one
        :return: A connection object
        """
        try:
            return self._q.get(True, initial_timeout)
        except Empty:
            try:
                self._lock.acquire()
                if self._cur_clients == self._max_clients:
                    raise ClientUnavailableError("Too many clients in use")
                cb = self._make_client()
                cb.start_using()
                return cb
            except ClientUnavailableError as ex:
                try:
                    # try to get a client again with a longer timeout
                    return self._q.get(True, next_timeout)
                except Empty:
                    logger.warn('Failed to get couchbase client, should consider increasing self._max_clients')
                    raise ex
            finally:
                self._lock.release()

    def release_client(self, cb):
        """
        Return a Connection object to the pool
        :param Connection cb: the client to release
        """
        if cb is not None:
            cb.stop_using()
            self._q.put(cb, True)

    def get_resultset_from_view(self, design, view, query=None):
        """
        :param design:
        :param view:
        :param query:
        :return:
        """
        client = None
        try:
            client = self.get_client()
            print 'Stats: last_use_time: %s, use_time: %s, use_count: %s' \
                  % (client.last_use_time, client.use_time, client.use_count)
            resultset = client.query(design, view, query=query)
        finally:
            self.release_client(client)

        return resultset

    def health_check(self):
        try:
            client = self.get_client()
            client.upsert(key='health_check', value='OK', ttl=5)
            status = client.get('health_check').value == 'OK'
            client.remove('health_check', quiet=True)
            self.release_client(client)
            return status
        except Exception as e:
            logger.error('Couchbase pool health check FAILED! Due to: %s' % e)
            return False