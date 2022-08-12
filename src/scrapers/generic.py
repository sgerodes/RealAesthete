from . import utils


class BaseSpider:

    @utils.cached_classproperty
    def name(cls):
        return cls.__name__
