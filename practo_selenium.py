__author__ = 'sunary'


from selenium import webdriver
# from utils.my_mongo import Mongodb
import re
import time


class PractoCrawl():

    def __init__(self):
        self.driver = webdriver.Firefox()
        # self.mongo = Mongodb(host='localhost', db='practo', col='url')

    def start(self):
        locations = ['bangalore', 'delhi', 'kolkata', 'pune', 'chennai', 'hyderabad', 'mumbai',
                     'Agra', 'Ahmedabad', 'Allahabad', 'Aurangabad', 'Bhopal', 'Chandigarh', 'Coimbatore', 'Ernakulam', 'Faridabad', 'Ghaziabad', 'Gurgaon', 'Indore', 'Jaipur', 'Jodhpur', 'Lucknow', 'Ludhiana', 'Meerut', 'Mohali', 'Nagpur', 'Nashik', 'Navi', 'Noida', 'Panchkula', 'Patna', 'Puducherry', 'Raipur', 'Surat', 'Thane', 'Thiruvananthapuram', 'Vadodara', 'Varanasi', 'Vijayawada', 'Visakhapatnam',
                     'singapore',
                     'batangas', 'metro-manila',
                     'jakarta',
                     'kuala-lumpur']

        index_urls = ['https://www.practo.com/bangalore/dentist?page=1',
                    'https://www.practo.com/bangalore/ophthalmologist?page=1',
                    'https://www.practo.com/bangalore/dermatologist-cosmetologist?page=1',
                    'https://www.practo.com/bangalore/homeopath?page=1',
                    'https://www.practo.com/bangalore/ayurveda?page=1',
                    'https://www.practo.com/bangalore/cardiologist?page=1',
                    'https://www.practo.com/bangalore/gastroenterologist?page=1',
                    'https://www.practo.com/bangalore/psychiatrist?page=1',
                    'https://www.practo.com/bangalore/ear-nose-throat-ENT-specialist?page=1',
                    'https://www.practo.com/bangalore/gynecologist-obstetrician?page=1',
                    'https://www.practo.com/bangalore/neurologist?page=1',
                    'https://www.practo.com/bangalore/urologist?page=1',

                    'https://www.practo.com/bangalore/diagnostics/tests?page=1',

                    'https://www.practo.com/bangalore/wellness-centers/spas?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/hair-cut-for-men?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/hair-cut-for-women?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/waxing?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/shaving?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/body-massage?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/facial?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/manicure?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/pedicure?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/threading?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/bleaching?page=1',
                    'https://www.practo.com/bangalore/wellness-centers/make-up?page=1',

                    'https://www.practo.com/bangalore/fitness-centers/gyms?page=1']
        for url in index_urls:
            for l in locations:
                self.crawl_url(url.replace(locations[0], l), l, re.match('.+/(.+?)\?.+', url).group(1))

    def crawl_url(self, input_url, location, subject):
        time.sleep(2)
        self.driver.get(input_url)
        list_urls = self.driver.find_elements_by_xpath('//div[@class="doc-details-block"]')
        for detail in list_urls:
            url_detail = re.search('href="(.+?)"', detail.get_attribute('innerHTML'))
            if url_detail:
                data = {'location': location,
                        'subject': subject,
                        'url': url_detail.group(1)}
                # self.mongo.insert(data)
                print data

        paginator = self.driver.find_element_by_xpath('//div[@class="paginator"]').get_attribute('innerHTML')
        if 'page_link page_link_next' in paginator:
            next_url = re.search('(.+=)[0-9]+$', input_url).group(1)
            next_url = next_url + str(int(input_url[len(next_url):]) + 1)
            # self.crawl_url(next_url, location, subject)

    def close(self):
        self.driver.close()


if __name__ == '__main__':
    practo = PractoCrawl()
    practo.start()
    practo.close()