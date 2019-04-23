from scrapy import cmdline
def run_spider():
    cmdline.execute('scrapy crawl ipproxy'.split())

if __name__ == '__main__':
    run_spider()