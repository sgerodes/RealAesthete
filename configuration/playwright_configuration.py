import asyncio
from twisted.internet import asyncioreactor, reactor
import sys


def configure_playwright():
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    else:
        asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

    asyncio.set_event_loop(asyncio.new_event_loop())
    #asyncioreactor.install(asyncio.get_event_loop())

    # set the reactor to use before importing Scrapy
    reactor.__class__ = asyncioreactor.AsyncioSelectorReactor

    import scrapy
    scrapy.utils.reactor.install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')