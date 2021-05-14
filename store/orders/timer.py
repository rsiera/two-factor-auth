from __future__ import unicode_literals

import logging
import time
from contextlib import contextmanager

from django.utils.encoding import smart_str

TIMER_MSG = '%(time)5.2fs | %(text)s'

logger = logging.getLogger(__name__)


@contextmanager
def timer(text):
    """
    Context manager that will log time of whatever it surrounds.
    First argument is text that is appended to log entry.
        with timer('request to "%s"' % url):
            request.get(url)
    """
    start = time.time()
    yield
    total = time.time() - start
    logger.info(TIMER_MSG, {'time': total, 'text': smart_str(text)})
