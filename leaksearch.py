import scrapy
import os
import hashlib
import re
from urllib.parse import urljoin

class LeaksearchSpider(scrapy.Spider):
    name = "leaksearch"

    def __init__(self):
        with open("targets.txt", "r") as f:
            self.targets = [line.strip().lower() for line in f if line.strip()]
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def start_requests(self):
        with open("onions.txt", "r") as f:
            for line in f:
                url = line.strip()
                if url.startswith("http://") or url.startswith("https://"):
                    yield scrapy.Request(
                        url=url,
                        callback=self.parse,
                        errback=self.errback_httpbin,
                        dont_filter=True
                    )

    def parse(self, response):
        url = response.url
        content = response.text.lower()

        # Save raw content to logs
        page_hash = hashlib.md5(url.encode()).hexdigest()
        log_path = f"logs/{page_hash}.html"
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(response.text)

        # Check for matches
        with open("leaks.txt", "r") as f:
            known = f.read()

        for target in self.targets:
            if re.search(re.escape(target), content):
                if f"{url} -> {target}" not in known:
                    self.logger.info(f"[+] Match found for: {target} in {url}")
                    with open("leaks.txt", "a") as f:
                        f.write(f"{url} -> {target}\n")
                break

        # Follow more onion links
        for href in response.css('a::attr(href)').getall():
            abs_url = urljoin(response.url, href)
            if ".onion" in abs_url and abs_url.startswith("http://"):
                yield scrapy.Request(
                    url=abs_url,
                    callback=self.parse,
                    errback=self.errback_httpbin,
                    dont_filter=True
                )

    def errback_httpbin(self, failure):
        self.logger.warning(f"[!] Error on {failure.request.url} -> {repr(failure.value)}")
