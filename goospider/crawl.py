from selenium import webdriver
import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
driver = webdriver.Chrome(ROOT_DIR+'chromedriver')
urls = ['https://www.google.com/search?q=23100107721',
        'https://www.google.com/search?q=41693392140',
        'https://www.google.com/search?q=49694260437',
        'https://www.google.com/search?q=641265232685',
        'https://www.google.com/search?q=797801035316',
        'https://www.google.com/search?q=14633149517',
        'https://www.google.com/search?q=20626716192',
        'https://www.google.com/search?q=45557180034',
        'https://www.google.com/search?q=43917231709'
        ]
for url in urls:
    driver.get("https://www.google.com/search?q=swat+strike")
    element = driver.find_element_by_xpath('//*[@id="resultStats"]/nobr')
    print element.text



    # def process_item(self, item, spider):
    #     self.file.writelines(["%s\n" % l for l in item['sellerurls']])
    #     data_fields = [i for i in item.iterkeys() if i != 'url' and i != 'condition' and i !='sellerurls']
    #     data = {}
    #     data['url'] = item['url']
    #     for field in data_fields:
    #         for idx, value in enumerate(item[field]):
    #             data[field + str(idx + 1)] = value
    #     return data
