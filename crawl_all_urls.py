import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
from collections import OrderedDict

locations = ['bangalore', 'delhi', 'kolkata', 'pune', 'chennai', 'hyderabad', 'mumbai', 'agra', 'ahmedabad',
             'allahabad', 'aurangabad', 'bhopal', 'chandigarh', 'coimbatore', 'ernakulam', 'faridabad', 'ghaziabad',
             'gurgaon', 'indore', 'jaipur', 'jodhpur', 'lucknow', 'ludhiana', 'meerut', 'mohali', 'nagpur', 'nashik',
             'navi', 'noida', 'panchkula', 'patna', 'puducherry', 'raipur', 'surat', 'thane', 'thiruvananthapuram',
             'vadodara', 'varanasi', 'vijayawada', 'visakhapatnam', 'singapore', 'batangas', 'metro-manila', 'jakarta',
             'kuala-lumpur']

index_urls = OrderedDict({
    'doctor': [
        'https://www.practo.com/%s/dentist?page=%s',
        'https://www.practo.com/%s/ophthalmologist?page=%s',
        'https://www.practo.com/%s/dermatologist-cosmetologist?page=%s',
        'https://www.practo.com/%s/homeopath?page=%s',
        'https://www.practo.com/%s/ayurveda?page=%s',
        'https://www.practo.com/%s/cardiologist?page=%s',
        'https://www.practo.com/%s/gastroenterologist?page=%s',
        'https://www.practo.com/%s/psychiatrist?page=%s',
        'https://www.practo.com/%s/ear-nose-throat-ENT-specialist?page=%s',
        'https://www.practo.com/%s/gynecologist-obstetrician?page=%s',
        'https://www.practo.com/%s/neurologist?page=%s',
        'https://www.practo.com/%s/urologist?page=%s'
    ],
    'diagnostic_lab': [
        'https://www.practo.com/%s/diagnostics/tests?page=%s',
        'https://www.practo.com/%s/diagnostics/thyroid-profile?page=%s',
        'https://www.practo.com/%s/diagnostics/lipid-profile?page=%s',
        'https://www.practo.com/%s/diagnostics/complete-blood-count?page=%s',
        'https://www.practo.com/%s/diagnostics/x-ray?page=%s',
        'https://www.practo.com/%s/diagnostics/hiv-1-2?page=%s',
        'https://www.practo.com/%s/diagnostics/pregnancy-test?page=%s',
        'https://www.practo.com/%s/diagnostics/urine-culture-and-sensitivity?page=%s',
        'https://www.practo.com/%s/diagnostics/stool-routine?page=%s',
        'https://www.practo.com/%s/diagnostics/ct-scan?page=%s',
        'https://www.practo.com/%s/diagnostics/semen-analysis?page=%s',
        'https://www.practo.com/%s/diagnostics/mri-scan?page=%s'
    ],
    'spa_and_salon': [
        'https://www.practo.com/%s/wellness-centers/spas?page=%s',
        'https://www.practo.com/%s/wellness-centers/hair-cut-for-men?page=%s',
        'https://www.practo.com/%s/wellness-centers/hair-cut-for-women?page=%s',
        'https://www.practo.com/%s/wellness-centers/waxing?page=%s',
        'https://www.practo.com/%s/wellness-centers/shaving?page=%s',
        'https://www.practo.com/%s/wellness-centers/body-massage?page=%s',
        'https://www.practo.com/%s/wellness-centers/facial?page=%s',
        'https://www.practo.com/%s/wellness-centers/manicure?page=%s',
        'https://www.practo.com/%s/wellness-centers/pedicure?page=%s',
        'https://www.practo.com/%s/wellness-centers/threading?page=%s',
        'https://www.practo.com/%s/wellness-centers/bleaching?page=%s',
        'https://www.practo.com/%s/wellness-centers/make-up?page=%s'

    ],
    'fitness': [
        'https://www.practo.com/%s/fitness-centers/gyms?page=%s'
    ]

})

mg_client = MongoClient()
collection = mg_client.practo.all_urls


def crawl_url(url, location, category):
    response = requests.get(url, verify=False)
    try:
        if response.status_code == requests.codes.ok:
            text = response.text
            page = BeautifulSoup(text, 'html.parser')
            links = page.find_all('a', {'class': 'doc-name'})
            if not links:
                return False
            for link in links:
                collection.save({
                    '_id': link['href'],
                    'loc': location,
                    'cat': category
                })
            return True
    except Exception as ex:
        print 'Something errors %s' % ex
        return True

    return False


def main():
    for loc in locations:
        for category, main_urls in index_urls.items():
            print 'Crawl category: %s' % category
            print main_urls
            for url in main_urls:
                print 'Main url: %s' % url
                for page_num in range(1, 1000000):
                    c_url = url % (loc, page_num)
                    print '***Crawling url***: %s' % c_url
                    if not crawl_url(c_url, loc, category):
                        break

    return


if __name__ == '__main__':
    main()
