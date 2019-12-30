import pstats

try:
    import cProfile as profile
except ImportError:
    import profile
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from django.conf import settings
from django.http import HttpResponse


class ProfilerMiddleware:
    """
    Simple profile middleware to profile django views. To run it, add ?prof to
    the URL like this:

        http://localhost:8000/view/?prof

    Optionally pass the following to modify the output:

    ?sort => Sort the output by a given metric. Default is time.
        See
        http://docs.python.org/2/library/profile.html#pstats.Stats.sort_stats
        for all sort options.

    ?count => The number of rows to display. Default is 100.

    ?download => Download profile file suitable for visualization. For example
        in snakeviz or RunSnakeRun

    This is adapted from an example found here:
    http://www.slideshare.net/zeeg/django-con-high-performance-django-presentation.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def _enable_profile(self, request):
        return settings.DEBUG and 'prof' in request.GET

    def process_view(self, request, view, args, kwargs):
        if self._enable_profile(request):
            profiler = profile.Profile()
            profiler.runcall(view, request, *args, **kwargs)
            # TODO: call process_exception on exceptions on above line
            # https://code.djangoproject.com/ticket/12250
            profiler.create_stats()
            if 'download' in request.GET:
                import marshal

                output = marshal.dumps(profiler.stats)
                response = HttpResponse(
                    output, content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment;' \
                                                  ' filename=view.prof'
                response['Content-Length'] = len(output)
            else:
                io = StringIO()
                stats = pstats.Stats(profiler, stream=io)

                stats.sort_stats(request.GET.get('sort', 'time'))
                stats.print_stats(int(request.GET.get('count', 100)))

                response = HttpResponse('<pre>%s</pre>' % io.getvalue())
            return response
