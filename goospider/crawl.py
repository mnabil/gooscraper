from selenium import webdriver
import os
from scrapy import Selector
from pyvirtualdisplay import Display

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

display = Display(visible=0, size=(800, 600))
display.start()


def clean_item(item):
    for k, v in item.items():
        if v is None:
            item[k] = u''


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

csv_headers = ['ID','Cost','Url', 'Store1', 'Price1', 'Extras1', 'Store2', 'Price2', 'Extras2', 'Store3', 'Price3', 'Extras3',
               'Store4', 'Price4', 'Extras4', 'Store5', 'Price5', 'Extras5', 'Store6', 'Price6', 'Extras6', 'Store7',
               'Price7', 'Extras7', 'Store8', 'Price8', 'Extras8', 'Store9', 'Price9', 'Extras9', 'Store10', 'Price10',
               'Extras10']
with open('data.csv', 'w') as f:
    f.write('\t'.join(csv_headers) + '\n')

    for url in urls:
        driver.get(url)
        print('Scraping URL: %s'%url)
        source = driver.page_source
        sel = Selector(text=source)
        rows = sel.css('._Dw')
        item = {}
        item['Url'] = unicode(url)

        for idx, select in enumerate(rows):
            item['Store' + str(idx + 1)] = select.css('a > .rhsg4').xpath('text()').extract_first()
            item['Price' + str(idx + 1)] = select.css('._kh').xpath('text()').extract_first().strip(u'$')
            item['Extras' + str(idx + 1)] = "\"" + select.css('._ree').xpath('normalize-space(string())').extract_first() +"\""
            item['ID'] = u''
            item['Cost'] = u''

        clean_item(item)
        print('Saving data into file: %s'%f.name)
        f.write(u'\t'.join([item[key] for key in csv_headers if key in item.keys()]).encode('utf-8') + '\n')

f.close()

driver.close()