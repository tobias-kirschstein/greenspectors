from argparse import ArgumentParser

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from greenspectors.env import DATA_PATH
from greenspectors.scraping.twitter_archive import TwitterArchiveSpider, TwitterSingleArchiveSpider

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--twitter_archive_name", type=str)
    args = parser.parse_args()

    # Setup Spider
    if args.twitter_archive_name is None:
        spider = TwitterArchiveSpider
        kwargs = dict()
    else:
        archive_name = args.twitter_archive_name
        spider = TwitterSingleArchiveSpider
        kwargs = {
            'archive_name': archive_name,
            'tmp_data_folder': f"{DATA_PATH}/tmp_data/{archive_name}"
        }

    # Setup Crawler
    settings = get_project_settings()
    settings['CONCURRENT_REQUESTS'] = 100
    settings['CONCURRENT_REQUESTS_PER_DOMAIN'] = 100

    process = CrawlerProcess(settings)
    process.crawl(spider, **kwargs)
    process.start()  # the script will block here until the crawling is finished



