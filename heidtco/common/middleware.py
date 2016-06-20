import logging
from StringIO import StringIO
from gzip import GzipFile
import re
import zlib

from ratelimit.utils import is_ratelimited

from django import http
from django.conf import settings
from django.core.handlers.wsgi import LimitedStream

logger = logging.getLogger(__name__)

class GunzipRequestMiddleware(object):
    encoding_gzip_re = re.compile(r'\bgzip\b')

    def process_request(self, request):
        encoding = request.META.get('HTTP_CONTENT_ENCODING', None)

        if encoding == 'gzip':
            if is_ratelimited(request, group='gunzip_request_middleware', key='ip', rate='300/1m', increment=True):
                return http.HttpResponse('Rate limit exceeded: too many gzipped request bodies', status=429)

            data = request._stream.read()
            if len(data) > settings.GUNZIP_MAX_COMPRESSED_SIZE:
                logger.warning('Compressed request body is too large: %s', request.path,
                    extra = {
                        'status_code': 400,
                        'request': request,
                    }
                )
                return http.HttpResponseBadRequest('Compressed request body is too large')

            try:
                zfile = GzipFile(mode='rb', fileobj=StringIO(data))
                uncompressed = zfile.read()
                request._stream = LimitedStream(StringIO(uncompressed), len(uncompressed))
                del request.META['HTTP_CONTENT_ENCODING']
            except IOError:
                return http.HttpResponseBadRequest('Invalid content-encoding, could not gunzip')

        return None
