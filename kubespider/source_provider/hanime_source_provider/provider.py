# This works for: https://hanime1.me/ or https://hanime.tv/
# Function: download search result
# encoding:utf-8

import subprocess

def install(package):
    subprocess.check_call(["pip", "install", package])

install("cloudscraper")

import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import cloudscraper

from source_provider import provider
from api import types
from api.values import Event, Resource
from utils.config_reader import AbsConfigReader
from utils import helper

class HanimeSourceProvider(provider.SourceProvider):
    def __init__(self, name: str, config_reader: AbsConfigReader) -> None:
        super().__init__(config_reader)
        self.provider_listen_type = types.SOURCE_PROVIDER_PERIOD_TYPE
        self.link_type = types.LINK_TYPE_GENERAL
        self.search_urls = []
        self.hanime_urls = []
        self.webhook_enable = True
        self.provider_type = 'hanime_source_provider'
        self.provider_name = name
        self.scraper = cloudscraper.create_scraper() 

    def get_provider_name(self) -> str:
        return self.provider_name

    def get_provider_type(self) -> str:
        return self.provider_type

    def get_provider_listen_type(self) -> str:
        return self.provider_listen_type

    def get_download_provider_type(self) -> str:
        return "hanihunter_download_provider"

    def get_download_param(self) -> dict:
        return self.config_reader.read().get('download_param', {})

    def get_prefer_download_provider(self) -> list:
        downloader_names = self.config_reader.read().get('downloader', None)
        if downloader_names is None:
            return None
        if isinstance(downloader_names, list):
            return downloader_names
        return [downloader_names]

    def get_link_type(self) -> str:
        return self.link_type

    def get_period_seconds(self) -> int:
        return self.config_reader.read().get('period_seconds', None)
    
    def get_cron_schedule(self) -> str:
        return self.config_reader.read().get('cron_schedule', None)

    def provider_enabled(self) -> bool:
        return self.config_reader.read().get('enable', True)

    def is_webhook_enable(self) -> bool:
        return self.webhook_enable

    def should_handle(self, event: Event) -> bool:
        parse_url = urlparse(event.source)
        if parse_url.hostname in ('hanime1.me', 'hanime.tv'):
            logging.info('%s belongs to hanime_source_provider', event.source)
            return True
        return False

    def get_links(self, event: Event) -> list[Resource]:
        self.get_hanime_url()
        ret = []
        for url in self.hanime_urls:
            logging.info('hanime find %s', helper.format_long_string(url))
            ret.append(Resource(
                url=url,
                path='',
                file_type=types.FILE_TYPE_COMMON,
                link_type=self.link_type,
            ))
        self.hanime_urls = []
        return ret

    def update_config(self, event: Event) -> None:
        pass

    def load_config(self) -> None:
        cfg = self.config_reader.read()
        logging.info('hanime search link is:%s', ','.join(cfg['search_url']))
        self.search_urls = cfg['search_url']

    def get_hanime_url(self):
        # example link: https://hanime1.me/search?genre=裏番
        if self.search_urls:
            try:
                for url in self.search_urls:
                    logging.info(f"Getting search result of {url}")
                    response = self.scraper.get(url)
                    if response.ok:
                        soup = BeautifulSoup(response.content, "html.parser")
                        videos = soup.find("div", {"class": "home-rows-videos-wrapper"}).find_all("a")
                        logging.info(f"Catch {len(videos)} hanimes video")
                        for video in videos:
                            link = video["href"]
                            self.hanime_urls.append(link)
            except Exception as e:
                logging.info(f"请求过程中出现错误：{str(e)}")