# -*- coding: utf-8 -*-
import scrapy
import logging
import random
from datetime import datetime
from time import sleep
from scrapy.selector import Selector
from ScrapySpiders.baseClassCareer import BaseSpiderCareer
from ScrapySpiders.baseClassCommon import configureLogging, getCustomSettings
from selenium.webdriver.common.keys import Keys

class ToptalentspiderSpider(scrapy.Spider, BaseSpiderCareer):
    name = 'toptalentspider'
    allowed_domains = ['www.toptalent.co']
    start_urls = ['https://toptalent.co/is-ilanlari/']
    logFileName = 'toptalent_spider_log.txt'
    configureLogging(logFileName)
    custom_settings = getCustomSettings("toptalent_ilan_Listesi %(time)s.csv")

    RESTART_WEBDRIVER_EVERY = 20
    WEBDRIVER_SLEEP_DURATION = 1 * 60

    def __init__(self):
        BaseSpiderCareer.__init__(self, logging, self.name)
        self.logging = logging
        self.category_name_error_num = [0]
        self.category_link_error_num = [0]
        self.advert_link_error_num = [0]
        self.title_error_num = [0]
        self.description_error_num = [0]
        self.job_description_error_num = [0]
        self.company_name_error_num = [0]
        self.gender_error_num = [0]
        self.age_error_num = [0]
        self.salary_error_num = [0]
        self.work_type_error_num = [0]
        self.city_error_num = [0]
        self.date_error_num = [0]
        self.education_error_num = [0]
        self.number_of_people_error_num = [0]
        self.number_of_view_error_num = [0]
        self.experience_error_num = [0]
        self.place_error_num = [0]
        self.sector_error_num = [0]
        self.job_names_error_num = [0]


    def parse(self, response):
        page_url= "https://www.toptalent.co/"
        page_link= "https://toptalent.co/is-ilanlari/"
        self.driver.get(page_link)
        self.driver.maximize_window()
        sleep(random.uniform(1, 3))
        self.checkPageSourceAndExit(self.driver.page_source, page_link)
        scrapy_selector = Selector(text=self.driver.page_source)
        sleep(2)

        next = True
        count=0
        while next == True:

            if count==0:
                for i in range(20):
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
                    sleep(0.1)
                scrapy_selector = Selector(text=self.driver.page_source)
                categories = scrapy_selector.xpath(
                             '//*[@id="AllJobs"]/div[1]/div[@class="row d-none d-sm-flex"]/div[@class="col-lg-4 col-md-6 col-12"]/div[@class="card card-job"]/a/@href').extract()
                print("categories:",categories)
                sleep(1)
                next_button = self.driver.find_element_by_xpath('//*[@id="PageNumbers"]/div/ul/li[5]/a')
                next_button.click()
                count+=1

            else:
                try:
                    for i in range(20):
                        self.driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)
                        sleep(0.1)
                    scrapy_selector = Selector(text=self.driver.page_source)
                    categories_new =scrapy_selector.xpath(
                                    '//*[@id="AllJobs"]/div[1]/div[@class="row d-none d-sm-flex"]/div[@class="col-lg-4 col-md-6 col-12"]/div[@class="card card-job"]/a/@href').extract()

                    categories.extend(categories_new)
                    print("categories_new:",categories_new)
                    print("len:",len(categories_new))
                    sleep(1)
                    next_button = self.driver.find_element_by_xpath('//*[@id="PageNumbers"]/div/ul/li[6]/a')
                except:
                    next=False
                    break
                next_button.click()
        categories = list(dict.fromkeys(categories))
        print('len:', len(categories))
        print("Categories: ", categories)

        scrapy_selector = Selector(text=self.driver.page_source)
        for i, url in enumerate(categories):
               self.driver.get(page_url + "/" + url)
               scrapy_selector = Selector(text=self.driver.page_source)

               company_name = scrapy_selector.xpath('/html/body/div[11]/div/div/div[2]/div[2]/div/h2/text()').extract()
               company_name = " ".join(company_name)
               title = scrapy_selector.xpath('/html/body/div[10]/div/div/div/h2/text()').extract()
               title = " ".join(title)
               description = scrapy_selector.xpath('/html/body/div[11]/div/div/div[1]/div/div/div//*[not(self::button)]/text()').extract()
               description = " ".join(description).replace('\n', ' ').split()
               description = " ".join(description)


               if company_name=='' and title=='' and description=='':
                   company_name = scrapy_selector.xpath(
                       '/html/body/div[16]/div/div/div[2]/div[1]/div/h2/text()').extract()
                   company_name = " ".join(company_name)
                   title = scrapy_selector.xpath('/html/body/div[9]/div/h1/text()').extract()
                   title = " ".join(title)
                   description = scrapy_selector.xpath(
                       '/html/body/div[10]/div/div/div[2]//text()').extract()+scrapy_selector.xpath(
                       '/html/body/div[11]/div/div/div[3]//text()').extract()+scrapy_selector.xpath(
                       '/html/body/div[12]/div/div//text()').extract()
                   description = " ".join(description).replace('\n', ' ').split()
                   description = " ".join(description)
               elif company_name=='' and title!='' and description!='':
                   company_name = scrapy_selector.xpath(
                       '/html/body/div[11]/div/div/div[2]/div/a/div/img[@class="d-inline-block img-fluid rounded"]/@alt').extract()
                   company_name = " ".join(company_name)


               print("company_name:", company_name)
               print("title:",title)
               print("description:", description)

               occupation = ""
               region = ""
               city = ""
               sector = ""
               contract_type = ""
               salary = ""
               work_type = ""
               responsibilities = ""
               education_level = ""
               experience = ""
               other_requirements = ""
               date_posted = ""
               age = ""
               gender = -1
               number_of_people = -1
               number_of_view = -1
               number_of_applyment = -1
               yield from self.saveScrappedCarrierInfo(web_site="toptalent",
                                                       title=str(title),
                                                       occupation=str(occupation),
                                                       country="Turkiye",
                                                       region=str(region),
                                                       city=str(city),
                                                       sector=str(sector),
                                                       company_name=str(company_name),
                                                       contract_type=str(contract_type),
                                                       salary=str(salary),
                                                       working_type=str(work_type),
                                                       responsibilities=str(responsibilities),
                                                       education_level=str(education_level),
                                                       job_description=str(description),
                                                       experience=str(experience),
                                                       other_requirements=str(other_requirements),
                                                       date_posted=str(date_posted),
                                                       number_of_view=int(number_of_view),
                                                       age=str(age),
                                                       gender=int(gender),
                                                       number_of_people=int(number_of_people),
                                                       number_of_applyment=int(number_of_applyment),
                                                       date_in_seconds=int(datetime.today().timestamp()))






