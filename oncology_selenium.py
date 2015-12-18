from selenium import webdriver
from utils.my_mongo import Mongodb
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from selenium.webdriver.common.by import By
from pyquery import PyQuery

__author__ = 'diepdt'


class OncologyCrawl(object):

    def __init__(self):
        # self.driver = webdriver.Firefox()
        self.mongo = Mongodb(host='localhost', db='dukemedicine', col='oncology')
        self.delay = 20
        self.col = Mongodb(host='localhost', db='dukemedicine', col='oncology_detail')

    def start(self):

        index_urls = ['https://www.dukemedicine.org/search-results/doctors?s=Oncology']
        for i in range(1, 39):
            index_urls.append('https://www.dukemedicine.org/search-results/doctors?s=Oncology&page=' + str(i))

        for url in index_urls:
            self.crawl_url(url)

    def wait(self, class_name):
        try:
            element = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                                                   class_name)))
            print " - Page is ready!"
            return element
        except TimeoutException:
            print " - Loading took too much time!"

    def crawl_url(self, input_url):
        print '***Start crawl ' + input_url
        self.driver.get(input_url)
        self.wait('result-title')
        links = self.driver.find_elements_by_class_name('result-title')
        if not links:
            print '+++ Url error: %s' % input_url
        links = [l.get_attribute('href') for l in links]
        for link in links:
            print '- Start crawl doctor ' + link
            self.driver.get(link)
            self.wait('mobileDoctorPhoneNumber')
            page = self.driver.page_source
            if not page:
                print '+++ Doctor link error %s' % link
            data = {'_id': link,
                    'page': page}
            self.mongo.save(data)

            print '- End crawl doctor ' + link

        print '***End crawl ' + input_url

    def close(self):
        self.driver.close()

    def process_page(self):
        for item in self.mongo.find(select=['page']):
            url = item['_id']
            print 'Process page ' + url
            html = item['page']
            jQuery = PyQuery(html)
            institute = 'Duke Cancer Institute'  # jQuery('.location-info a.result-title').text().strip()
            img_url_destop = jQuery('.desktopPic').attr('src')
            img_url_mobile = jQuery('.mobilePic').attr('src')
            name_and_spec = jQuery('.nameAndSpecialties').find('.header1').text()
            name_degree = [x.strip() for x in name_and_spec.split(',')]
            name = name_degree[0]
            degree = ', '.join(name_degree[1:])
            inner_name = name
            first_name = name[:name.find(' ')].strip()
            last_name = name[name.find(' '):].strip()
            appointment = jQuery('.appointment-number .doctorPhoneNumber .phoneHelperText').text().strip()
            address = jQuery('.location-info p.address').text().strip()
            city_state_zip = jQuery('.location-info .cityStateZip'). text().strip()
            location = jQuery('.location-info a.result-title').text().strip() + '\n' + address + ',' + '\n' + city_state_zip
            zipcode = city_state_zip[city_state_zip.rfind(' '):].strip()
            bio = jQuery('.aboutText').text().strip()
            specialty = jQuery('.specialties').text().strip()
            research_interests = jQuery('.researchText').text().strip()
            education = jQuery('.trainingSection .training-description .plainText').eq(0).text().strip()
            residency = jQuery('.trainingSection .training-description .plainText').eq(1).text().strip()
            fellowship = jQuery('.trainingSection .training-description .plainText').eq(2).text().strip()
            training = residency + '\n' + fellowship
            certification = jQuery('.trainingSection').eq(3).find('.plainText').text().strip()
            phone = jQuery('.appointment-number .doctorPhoneNumber span.doctor-phone').text().strip()
            office_phone = jQuery('.phone-numbers .mobile-only .doctor-phone').text().strip()
            fax_number = jQuery('.phone-numbers .faxNumber .doctor-phone').text().strip()
            industry = jQuery('.industry-relations .plainText').eq(0).text()

            detail = dict(
                _id=url,
                url=url,
                institute=institute,
                img_url_destop=img_url_destop,
                img_url=img_url_destop,
                img_url_mobile=img_url_mobile,
                name_and_spec=name_and_spec,
                degree=degree,
                inner_name=inner_name,
                last_name=last_name,
                first_name=first_name,
                appointment=appointment,
                location=location,
                city_state_zip=city_state_zip,
                zipcode=zipcode,
                specialty=specialty,
                bio=bio,
                research_interests=research_interests,
                education=education,
                residency=residency,
                fellowship=fellowship,
                training=training,
                certification=certification,
                phone=phone,
                office_phone=office_phone,
                fax_number=fax_number,
                industry=industry
            )

            self.col.save(detail)

    def export_to_csv(self):
        self.col.export_csv(fields=['url', 'institute', 'img_url_destop', 'img_url', 'img_url_mobile', 'name_and_spec',
                                    'degree', 'inner_name', 'last_name', 'first_name', 'location',
                                    'city_state_zip', 'zipcode', 'specialty', 'bio', 'research_interests',
                                    'education', 'residency', 'fellowship', 'training', 'certification', 'phone',
                                    'office_phone', 'fax_number', 'industry'], output='151218_oncology.csv')


if __name__ == '__main__':
    oncology = OncologyCrawl()
    # oncology.start()
    # oncology.close()
    # oncology.process_page()
    oncology.export_to_csv()
