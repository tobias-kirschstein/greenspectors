import bz2
import json
from json import JSONDecodeError
from pathlib import Path

from scrapy import Spider, Request

from greenspectors.data.dataset_writer import BufferedDatasetWriter
from greenspectors.env import DATA_PATH, TWITTER_ARCHIVE_DATASET_PATH, COMPANY_NAMES, SYNONYMS
from greenspectors.util.io import parse_size_to_mb, download_file


class TwitterSingleArchiveSpider(Spider):
    def __init__(self,
                 archive_name: str,
                 tmp_data_folder: str = f"{DATA_PATH}/tmp_data",
                 dataset_writer: BufferedDatasetWriter = None):
        super(TwitterSingleArchiveSpider, self).__init__(name="Twitter Single Archive Spider")
        self._tmp_data_folder = tmp_data_folder
        Path(tmp_data_folder).mkdir(exist_ok=True, parents=True)

        if dataset_writer is None:
            output_path = f"{TWITTER_ARCHIVE_DATASET_PATH}/{archive_name}"
            Path(output_path).mkdir(exist_ok=True, parents=True)
            self._dataset_writer = BufferedDatasetWriter(output_path,
                                                         dataset_slice_size=100000)
        else:
            self._dataset_writer = dataset_writer
        self._json_urls = []

        self._company_name_synonyms = [synonym.lower()
                                       for company_name in COMPANY_NAMES
                                       for synonym in [company_name] + SYNONYMS[company_name]]

        self._archive_name = archive_name

    def closed(self, reason):
        self._dataset_writer.finish()

    def start_requests(self):
        yield Request(url=f"https://archive.org/download/{self._archive_name}", callback=self.parse_download_page)

    def parse_download_page(self, response):
        sizes = response.css('table.directory-listing-table tr td:last-child::text').getall()
        sizes = [parse_size_to_mb(size) for size in sizes]

        file_links = response.css(
            'table.directory-listing-table tr td:first-child a:first-child::attr(href)').getall()[
                     1:]  # Ignore first link, as it just points back to parent directory
        file_urls = [f"{response.url}/{file}/" for file, size in zip(file_links, sizes) if 100 < size < 5000]

        for file_url in file_urls:
            yield Request(file_url, callback=self.parse_archive_listing)

    def parse_archive_listing(self, response):
        single_json_urls = response.css('table.archext tr td a::attr(href)').getall()
        single_json_urls = [f"https:{json_url}" for json_url in single_json_urls]
        self._json_urls.extend(single_json_urls)

        for url in single_json_urls:
            yield Request(url, callback=self.parse_bz_file)

    def parse_bz_file(self, response):
        json_file = bz2.decompress(response.body)
        for line in json_file.splitlines():
            self._process_tweet(line)

    def _process_tweet(self, tweet_json: bytes):
        try:
            tweet = json.loads(tweet_json)
            # Only use english tweets
            if 'text' in tweet and 'lang' in tweet and tweet['lang'] == 'en':
                tweet_text = tweet['text'].lower()
                for company_name_synonym in self._company_name_synonyms:
                    if company_name_synonym in tweet_text:
                        # Any of the company names matched
                        self._dataset_writer.add(tweet_json)
                        print(f"Found tweets: {len(self._dataset_writer)}")
                        break
        except JSONDecodeError as e:
            print(f"Error parsing tweet {tweet_json}: {e}")


class TwitterArchiveSpider(Spider):
    def __init__(self, tmp_data_folder: str = f"{DATA_PATH}/tmp_data"):
        super(TwitterArchiveSpider, self).__init__(name="Twitter Archive Spider")
        self._tmp_data_folder = tmp_data_folder
        Path(tmp_data_folder).mkdir(exist_ok=True, parents=True)

        self._dataset_writer = BufferedDatasetWriter(TWITTER_ARCHIVE_DATASET_PATH, dataset_slice_size=1000)

    def start_requests(self):
        urls = [
            "https://archive.org/details/twitterstream?&sort=-week&page=1",
            "https://archive.org/details/twitterstream?&sort=-week&page=2"
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        archive_links = response.css("div.results div.item-ia div.C234 a::attr(href)").getall()
        archive_names = [Path(archive_link).stem for archive_link in archive_links]

        for archive_name in archive_names:
            single_archive_scraper = TwitterSingleArchiveSpider(archive_name,
                                                                self._tmp_data_folder,
                                                                dataset_writer=self._dataset_writer)
            for request in single_archive_scraper.start_requests():
                yield request


# TODO: Actually there are also datasets for 2021-09/2021-08 etc... They are just not listed
# archiveteam-twitter-stream-2021-07
# archiveteam-twitter-stream-2021-05
# archiveteam-twitter-stream-2021-03
# archiveteam-twitter-stream-2021-01
# archiveteam-twitter-stream-2020-11
# archiveteam-twitter-stream-2020-10
# archiveteam-twitter-stream-2020-07
# archiveteam-twitter-stream-2020-02
# archiveteam-twitter-stream-2018-12
# archiveteam-twitter-stream-2018-09
# archiveteam-twitter-stream-2018-07
# archiveteam-twitter-stream-2018-05
# archiveteam-twitter-stream-2018-04
# archiveteam-twitter-stream-2018-02
# archiveteam-twitter-stream-2017-09
# archiveteam-twitter-stream-2017-06
# archiveteam-twitter-stream-2017-05
# archiveteam-twitter-stream-2017-04
# archiveteam-twitter-stream-2016-09
# archiveteam-twitter-stream-2016-04
# archiveteam-twitter-stream-2015-09
# archiveteam-twitter-stream-2014-11
#
# archiveteam-twitter-stream-2012-03
# archiveteam-twitter-stream-2012-04
#
#
# archiveteam-twitter-stream-2013-05
#
#
# archiveteam-twitter-stream-2012-05
#
# archiveteam-twitter-stream-2015-11
# archiveteam-twitter-stream-2016-08
#
#
# archiveteam-twitter-stream-2013-12
# archiveteam-twitter-stream-2013-03
# archiveteam-twitter-stream-2014-04
# archiveteam-twitter-stream-2015-12
#
#
#
#
# archiveteam-twitter-stream-2015-05
#
#
#
# archiveteam-twitter-stream-2016-10
# archiveteam-twitter-stream-2012-12
# archiveteam-twitter-stream-2013-10
#
#
#
# archiveteam-twitter-stream-2013-09
# archiveteam-twitter-stream-2012-09