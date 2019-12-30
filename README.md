# django-cprofile-middleware

This middleware allows you to profile performance in Django applications.

Add ```?prof``` to your URL. Then instead of showing the requested page, Django will show the cProfile output.

This will show a row for each method called, with the following stats:
* number of times it was called (ncalls)
* how much time was spent per call (percall)
* how much time was spent total in that method (cumtime)
* file and line number

This is helpful in finding performance optimizations in your Django application.

This is a fork of [this project](https://github.com/omarish/django-cprofile-middleware) with several changes:
* Support for Django 2.1
* Remove backwards compatibility with Django <= 1.10
* Remove the ```DJANGO_CPROFILE_MIDDLEWARE_REQUIRE_STAFF``` setting
* Always show the absolute file path rather than filename

## Installing

```bash
$ pip install -e git+https://github.com/dgmdan/django-cprofile-middleware.git@master#egg=django_cprofile_middleware
```

Then add ```django_cprofile_middleware.middleware.ProfilerMiddleware``` to the end your ```MIDDLEWARE``` in settings.py.

For example:

```
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'startup.do.work.FindProductMarketFitMiddleware',
    ...
    'django_cprofile_middleware.middleware.ProfilerMiddleware'
]
```

## Running & Sorting Results

Once you've installed it, add ```?prof``` to any URL to see the profiler's stats. For example to see profile stats for ```http://localhost:8000/foo/```, visit ```http://localhost:8000/foo/?prof```.

Note that ```DEBUG``` settings must be set to ```True```.

You can also pass some options:

**count:** The number of results you'd like to see. Default is 100.

**sort:** The field you'd like to sort results by. Default is ```time```. For all the options you can pass, see the [docs for pstats](http://docs.python.org/2/library/profile.html#pstats.Stats.sort_stats).

**download:** Download profile file, that can be visualized in multiple viewers, e.g. [SnakeViz](https://github.com/jiffyclub/snakeviz/) or [RunSnakeRun](http://www.vrplumber.com/programming/runsnakerun/)
