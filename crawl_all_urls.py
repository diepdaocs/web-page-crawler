import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

locations = ['bangalore', 'delhi', 'kolkata', 'pune', 'chennai', 'hyderabad', 'mumbai', 'agra', 'ahmedabad',
             'allahabad', 'aurangabad', 'bhopal', 'chandigarh', 'coimbatore', 'ernakulam', 'faridabad', 'ghaziabad',
             'gurgaon', 'indore', 'jaipur', 'jodhpur', 'lucknow', 'ludhiana', 'meerut', 'mohali', 'nagpur', 'nashik',
             'navi', 'noida', 'panchkula', 'patna', 'puducherry', 'raipur', 'surat', 'thane', 'thiruvananthapuram',
             'vadodara', 'varanasi', 'vijayawada', 'visakhapatnam', 'singapore', 'batangas', 'metro-manila', 'jakarta',
             'kuala-lumpur']

index_urls = {
    'doctor': [
        'https://www.practo.com/%s/dentist?page=%',
        'https://www.practo.com/%s/ophthalmologist?page=%',
        'https://www.practo.com/%s/dermatologist-cosmetologist?page=%',
        'https://www.practo.com/%s/homeopath?page=%',
        'https://www.practo.com/%s/ayurveda?page=%',
        'https://www.practo.com/%s/cardiologist?page=%',
        'https://www.practo.com/%s/gastroenterologist?page=%',
        'https://www.practo.com/%s/psychiatrist?page=%',
        'https://www.practo.com/%s/ear-nose-throat-ENT-specialist?page=%',
        'https://www.practo.com/%s/gynecologist-obstetrician?page=%',
        'https://www.practo.com/%s/neurologist?page=%',
        'https://www.practo.com/%s/urologist?page=%'
    ],
    'diagnostic_lab': [
        'https://www.practo.com/%s/diagnostics/tests?page=%',
        'https://www.practo.com/%s/diagnostics/thyroid-profile?page=%',
        'https://www.practo.com/%s/diagnostics/lipid-profile?page=%',
        'https://www.practo.com/%s/diagnostics/complete-blood-count?page=%',
        'https://www.practo.com/%s/diagnostics/x-ray?page=%',
        'https://www.practo.com/%s/diagnostics/hiv-1-2?page=%',
        'https://www.practo.com/%s/diagnostics/pregnancy-test?page=%',
        'https://www.practo.com/%s/diagnostics/urine-culture-and-sensitivity?page=%',
        'https://www.practo.com/%s/diagnostics/stool-routine?page=%',
        'https://www.practo.com/%s/diagnostics/ct-scan?page=%',
        'https://www.practo.com/%s/diagnostics/semen-analysis?page=%',
        'https://www.practo.com/%s/diagnostics/mri-scan?page=%'
    ],
    'spa_and_salon': [
        'https://www.practo.com/%s/wellness-centers/spas?page=%',
        'https://www.practo.com/%s/wellness-centers/hair-cut-for-men?page=%',
        'https://www.practo.com/%s/wellness-centers/hair-cut-for-women?page=%',
        'https://www.practo.com/%s/wellness-centers/waxing?page=%',
        'https://www.practo.com/%s/wellness-centers/shaving?page=%',
        'https://www.practo.com/%s/wellness-centers/body-massage?page=%',
        'https://www.practo.com/%s/wellness-centers/facial?page=%',
        'https://www.practo.com/%s/wellness-centers/manicure?page=%',
        'https://www.practo.com/%s/wellness-centers/pedicure?page=%',
        'https://www.practo.com/%s/wellness-centers/threading?page=%',
        'https://www.practo.com/%s/wellness-centers/bleaching?page=%',
        'https://www.practo.com/%s/wellness-centers/make-up?page=%'

    ],
    'fitness': [
        'https://www.practo.com/%s/fitness-centers/gyms'
    ]

}

mg_client = MongoClient()
collection = mg_client.practo.all_urls


def crawl_url(url, location, category):
    response = requests.get(url, verify=False)
    try:
        if response.status_code == requests.codes.ok:
            text = response.text
            page = BeautifulSoup(text, 'html_parser')
            links = page.find_all('a', {'class': 'doc-name'})
            for link in links:
                collection.save({
                    '_id': link['href'],
                    'loc': location,
                    'cat': category
                })
            return True
    except Exception as ex:
        print 'Somthing errors %s' % ex
        return True

    return False


def main():
    for loc in locations:
        for category, main_urls in index_urls.items():
            print 'Crawl category %s' % category
            for url in main_urls:
                for page_num in range(1, 1000000):
                    url = url % (loc, page_num)
                    print 'Crawling url %s' % url
                    if not crawl_url(url, loc, category):
                        break

    return


if __name__ == '__main__':
    main()
