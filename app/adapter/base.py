import time
from setting import setting


def detect_slow_call(request_at, url, is_slow, _logger):
    request_time = (time.time() - request_at) * 1000
    _logger.info('Calling to URL: %s took %f ms' % (url, request_time))
    if request_time > setting.SLOW_SERVICE_CALL_MS and not is_slow:
        _logger.warning('[SLOW CALL %f ms]%s' % (request_time, url))
