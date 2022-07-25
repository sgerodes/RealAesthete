from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


def run_parallel_spiders(spiders, project_settings):
    for s in spiders:
        runner = CrawlerRunner(settings=project_settings)
        runner.crawl(s)

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()


def run_parallel_spiders_2(spiders_and_settings):
    for s in spiders_and_settings:
        spider = s[0]
        settings = s[1]
        runner = CrawlerRunner(settings=settings)
        runner.crawl(spider)

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()
