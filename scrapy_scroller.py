import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
from selenium.webdriver.chrome.options import Options
from shutil import which
import time

"""
To scrape webpages that use scrollers to continously load new content 

NOTE: Require selenium library and selenium chromedriver to be downloaded and stored in the same location as the scrapy.cfg file 
"""
 
class ActSpider(scrapy.Spider):
    name = 'ACT'
    start_urls = [
        'https://sso.agc.gov.sg/Act/ACRAA2004'
    ] #change url 
 
    def __init__(self): #add the codes below into the existing constructor function of the existing scraper
        chrome_options = Options()
        chrome_path = which('chromedriver')
 
        # settings for seleium 
        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.set_window_size(1920, 1080)
        driver.get("https://sso.agc.gov.sg/Act/ACRAA2004") #Change url
 
        # code for scroller to scroll down the webpage 
        number_scrolls = 10
        i = 0
        while i < number_scrolls:
            # Scroll down to bottom
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            i+=1
            time.sleep(2)

        self.html = driver.page_source
        driver.close()
 
    def parse(self, response): #to scrape text in each Part of each ACT
        resp = Selector(text=self.html)
        for table in resp.xpath("//div[@class='body']/table"): # to loop through each Part in each ACT 
            yield {
                'info': table.xpath('.//text()').getall()
            }
