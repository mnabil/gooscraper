from selenium import webdriver
import os

from pyvirtualdisplay import Display
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

display = Display(visible=0, size=(800, 600))
display.start()

driver = webdriver.Firefox()
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
data = {}
for url in urls:
    driver.get(url)
    element = driver.find_element_by_xpath('//*[@id="resultStats"]/nobr')
    print element.text
driver.close()


    # def process_item(self, item, spider):
    #     self.file.writelines(["%s\n" % l for l in item['sellerurls']])
    #     data_fields = [i for i in item.iterkeys() if i != 'url' and i != 'condition' and i !='sellerurls']
    #     data = {}
    #     data['url'] = item['url']
    #     for field in data_fields:
    #         for idx, value in enumerate(item[field]):
    #             data[field + str(idx + 1)] = value
    #     return data
