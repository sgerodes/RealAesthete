from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor


def run_parallel_spiders(spiders, project_settings):
    for s in spiders:
        runner = CrawlerRunner(settings=project_settings)
        runner.crawl(s)

    deferred = runner.join()
    deferred.addBoth(lambda _: reactor.stop())
    reactor.run()
