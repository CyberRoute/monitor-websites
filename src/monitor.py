import requests
import json
from socket import gaierror, gethostbyname
import concurrent.futures
import threading
from urllib.parse import urlparse
from datetime import datetime
from config.config import Config
import logging

logging.basicConfig(filename='../record.log',
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


class Monitor:

    @staticmethod
    def is_alive(url):
        """ This function checks to see if a host name has a DNS entry
        by checking for socket info."""
        try:
            gethostbyname(url)
        except gaierror:
            return False
        else:
            return True

    @staticmethod
    def get_statuses(url):
        """ This function returns the status, time_elapsed, timestamp, lastupdate"""
        try:
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            lastupdate = datetime.now().strftime('%y-%m-%d %a %H:%M:%S')
            response = requests.get(url, timeout=30)
            requests.session().close()
            status = response.status_code
            time_elapsed = response.elapsed.total_seconds()
            return status, time_elapsed, timestamp, lastupdate
        except requests.ConnectionError:
            return Config.DOWN

    @staticmethod
    def check_single_url(url):
        """This function checks a single url"""
        if Monitor.is_alive(urlparse(url).hostname):
            return Monitor.get_statuses(url)
        else:
            return Config.DOWN

    @staticmethod
    def launch_checker():
        """This function launches the check_multiple_urls function every x seconds
        (defined in refresh interval variable)."""
        t = threading.Timer(Config.REFRESH, Monitor.check_multiple_urls)
        t.daemon = True
        t.start()
        results = Monitor.check_multiple_urls()
        return results

    @staticmethod
    def check_multiple_urls():
        """This function checks through urls specified in the urls.json file
        (specified in the filename variable) and
        returns their statuses as a dictionary."""
        statuses = {}
        urls = Monitor.generate_list_urls(Monitor.open_url_file())
        with concurrent.futures.ThreadPoolExecutor(max_workers=Config.PROCS) as executor:
            results = executor.map(Monitor.check_single_url, urls)
        finals = []
        for v in results:
            finals.append(v)
        for i in range(len(urls)):
            statuses[urls[i]] = (finals[i])
        return statuses

    @staticmethod
    def https_start_strip(url):
        """This function strip a url"""
        url = url.strip().lower()
        if url[:7] == 'http://':
            return url
        elif url[:8] == 'https://':
            return url
        else:
            url = "https://" + url
            return url

    @staticmethod
    def generate_list_urls(urls_dict):
        """This function generate a list of urls"""
        list_urls = []
        for group, urls in urls_dict.items():
            for url in urls:
                list_urls.append(url)
        return list_urls

    @staticmethod
    def open_url_file():
        """This function open and read the urls.json file"""
        with open(Config.URLS) as f:
            checkurls = json.load(f)
        return checkurls
