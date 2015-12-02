__author__ = 'sunary'


from selenium import webdriver
from utils.my_mongo import Mongodb
import re
import time


class PractoCrawl():

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.mongo = Mongodb(host='localhost', db='practo', col='url')

    def start(self):
        index_urls = ['https://www.practo.com/bangalore/dentist?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/ophthalmologist?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/dermatologist-cosmetologist?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/homeopath?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/ayurveda?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/cardiologist?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/gastroenterologist?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/psychiatrist?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/ear-nose-throat-ENT-specialist?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/gynecologist-obstetrician?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/neurologist?filters[min_fee]=0&filters[max_fee]=1500&page=1',
                    'https://www.practo.com/bangalore/urologist?filters[min_fee]=0&filters[max_fee]=1500&page=1']

        for url in index_urls[:1]:
            self.crawl_url(url, re.search('bangalore/(.+)\?', url).group(1))

    def crawl_url(self, input_url, subject):
        time.sleep(2)
        self.driver.get(input_url)
        list_urls = self.driver.find_elements_by_xpath('//div[@class="doc-details-block"]')
        for detail in list_urls:
            url_detail = re.search('href="(.+?)"', detail.get_attribute('innerHTML'))
            if url_detail:
                data = {'subject': subject,
                        'url': url_detail}
                self.mongo.insert(data)

        paginator = self.driver.find_element_by_xpath('//div[@class="paginator"]').get_attribute('innerHTML')
        if 'page_link page_link_next' in paginator:
            next_url = re.search('(.+=)[0-9]+$', input_url).group(1)
            next_url = next_url + str(int(input_url[len(next_url):]) + 1)
            self.crawl_url(next_url, subject)

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    practo = PractoCrawl()
    practo.start()
    practo.close()