from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pymysql
import numpy
import time
import datetime

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

chromedriver = 'C:/Users/PARK/Desktop/Analysis/Danawa/code/chromedriver.exe'
driver = webdriver.Chrome(chromedriver, options = options)

url = 'http://shop.danawa.com/pc/?controller=estimateDeal&methods=estimateform'
driver.get(url)

driver.switch_to.frame('IFRAME_SrchOption')
ram_page_xpath = '/html/body/form/div/div[1]/div[1]/div[2]/ul[1]/li[4]/a'
driver.find_element_by_xpath(ram_page_xpath).click()

driver.switch_to.default_content()
driver.switch_to.frame('IFRAME_ProdList')


class DBConnect:
    def __init__(self):
        self.conn = pymysql.connect(host = 'localhost', user = 'root', password = '4643' , db = 'danawa', charset = 'utf8')
        self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
    
    def insert(self, date, hour, rank, name, price, release, clock, brand, gen, purpose):
        try:
            sql = """INSERT INTO ram(CRAWL_DATE, HOUR, RANKING, NAME, PRICE, RELEASE_DATE, CLOCK, BRAND, GEN, PURPOSE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            
            for i in range(50):
                
                self.curs.execute(sql, (date, hour, i+1, name[i], price[i], release[i], clock[i], brand[i], gen[i], purpose[i]))
            
            self.conn.commit()
            
        except Exception as e:
            print(e)
        
        finally:
            self.conn.close()

def main():
    crawl_date = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
    crawl_time = datetime.datetime.now().hour

    product_name_list = []
    product_price_list = []
    product_enroll_list = []
    product_gen_list = []
    product_clock_list = []
    product_purpose_list = []

    name_xpath = "/html/body/form/div/div[2]/ul/li[{}]/div/div[2]/div[1]/a"
    price_xpath = "/html/body/form/div/div[2]/ul/li[{}]/div/div[3]/div/dl/dd/span"
    enroll_xpath = "/html/body/form/div/div[2]/ul/li[{}]/div/div[2]/div[2]/dl/dd"
    gen_xpath = "/html/body/form/div/div[2]/ul/li[{}]/div/div[2]/dl/dd/ul/li[1]"
    clock_xpath = "/html/body/form/div/div[2]/ul/li[{}]/div/div[2]/dl/dd/ul/li[4]"
    purpose_xpath = "/html/body/form/div/div[2]/ul/li[{}]/div/div[2]/dl/dd/ul/li[2]"

    for i in range(1, 4):
        print("Page: {}\n".format(i))
        page_xpath = "/html/body/form/div/div[3]/div/a[{}]".format(i)
        time.sleep(3)
        driver.find_element_by_xpath(page_xpath).click()
        time.sleep(0.5)
        
        if i == 1:
            for j in range(1, 23):
                product_name_xpath = name_xpath.format(j)
                product_price_xpath = price_xpath.format(j)
                product_enroll_xpath = enroll_xpath.format(j)
                product_gen_xpath = gen_xpath.format(j)
                product_clock_xpath = clock_xpath.format(j)
                product_purpose_xpath = purpose_xpath.format(j)

                try:
                    product_name = driver.find_element_by_xpath(product_name_xpath)
                    product_price = driver.find_element_by_xpath(product_price_xpath)
                    product_enroll = driver.find_element_by_xpath(product_enroll_xpath)
                    product_gen = driver.find_element_by_xpath(product_gen_xpath)
                    product_clock = driver.find_element_by_xpath(product_clock_xpath)
                    product_purpose = driver.find_element_by_xpath(product_purpose_xpath)

                    print(product_name.text,"\n",product_price.text,"\n",product_gen.text,"\n",product_clock.text,"\n",product_enroll.text)

                    product_price_list.append(product_price.text)

                except NoSuchElementException:
                    product_name = driver.find_element_by_xpath(product_name_xpath)
                    product_enroll = driver.find_element_by_xpath(product_enroll_xpath)
                    product_gen = driver.find_element_by_xpath(product_gen_xpath)
                    product_clock = driver.find_element_by_xpath(product_clock_xpath)
                    product_purpose = driver.find_element_by_xpath(product_purpose_xpath)
                    
                    print(product_name.text,"\n","0","\n",product_gen.text,"\n",product_clock.text,"\n",product_enroll.text)

                    product_price_list.append('0')
                    
                product_name_list.append(product_name.text)
                product_enroll_list.append(product_enroll.text)
                product_gen_list.append(product_gen.text)
                product_clock_list.append(product_clock.text)
                product_purpose_list.append(product_purpose.text)
                
                time.sleep(1)

        elif i == 2:
            for j in range(1, 21):
                product_name_xpath = name_xpath.format(j)
                product_price_xpath = price_xpath.format(j)
                product_enroll_xpath = enroll_xpath.format(j)
                product_gen_xpath = gen_xpath.format(j)
                product_clock_xpath = clock_xpath.format(j)
                product_purpose_xpath = purpose_xpath.format(j)

                try:
                    product_name = driver.find_element_by_xpath(product_name_xpath)
                    product_price = driver.find_element_by_xpath(product_price_xpath)
                    product_enroll = driver.find_element_by_xpath(product_enroll_xpath)
                    product_gen = driver.find_element_by_xpath(product_gen_xpath)
                    product_clock = driver.find_element_by_xpath(product_clock_xpath)
                    product_purpose = driver.find_element_by_xpath(product_purpose_xpath)

                    print(product_name.text,"\n",product_price.text,"\n",product_gen.text,"\n",product_clock.text,"\n",product_enroll.text)

                    product_price_list.append(product_price.text)

                except NoSuchElementException:
                    product_name = driver.find_element_by_xpath(product_name_xpath)
                    product_enroll = driver.find_element_by_xpath(product_enroll_xpath)
                    product_gen = driver.find_element_by_xpath(product_gen_xpath)
                    product_clock = driver.find_element_by_xpath(product_clock_xpath)
                    product_purpose = driver.find_element_by_xpath(product_purpose_xpath)
                    
                    print(product_name.text,"\n","0","\n",product_gen.text,"\n",product_clock.text,"\n",product_enroll.text)

                    product_price_list.append('0')
                    
                product_name_list.append(product_name.text)
                product_enroll_list.append(product_enroll.text)
                product_gen_list.append(product_gen.text)
                product_clock_list.append(product_clock.text)
                product_purpose_list.append(product_purpose.text)
                
                time.sleep(1)

        elif i == 3:
            for j in range(1, 9):
                product_name_xpath = name_xpath.format(j)
                product_price_xpath = price_xpath.format(j)
                product_enroll_xpath = enroll_xpath.format(j)
                product_gen_xpath = gen_xpath.format(j)
                product_clock_xpath = clock_xpath.format(j)
                product_purpose_xpath = purpose_xpath.format(j)

                try:
                    product_name = driver.find_element_by_xpath(product_name_xpath)
                    product_price = driver.find_element_by_xpath(product_price_xpath)
                    product_enroll = driver.find_element_by_xpath(product_enroll_xpath)
                    product_gen = driver.find_element_by_xpath(product_gen_xpath)
                    product_clock = driver.find_element_by_xpath(product_clock_xpath)
                    product_purpose = driver.find_element_by_xpath(product_purpose_xpath)

                    print(product_name.text,"\n",product_price.text,"\n",product_gen.text,"\n",product_clock.text,"\n",product_enroll.text)

                    product_price_list.append(product_price.text)

                except NoSuchElementException:
                    product_name = driver.find_element_by_xpath(product_name_xpath)
                    product_enroll = driver.find_element_by_xpath(product_enroll_xpath)
                    product_gen = driver.find_element_by_xpath(product_gen_xpath)
                    product_clock = driver.find_element_by_xpath(product_clock_xpath)
                    product_purpose = driver.find_element_by_xpath(product_purpose_xpath)

                    print(product_name.text,"\n","0","\n",product_gen.text,"\n",product_clock.text,"\n",product_enroll.text)

                    product_price_list.append('0')
                    
                product_name_list.append(product_name.text)
                product_enroll_list.append(product_enroll.text)
                product_gen_list.append(product_gen.text)
                product_clock_list.append(product_clock.text)
                product_purpose_list.append(product_purpose.text)
                
                time.sleep(1)

    driver.quit()
        
    brand_list = [x.split(" ")[0] for x in product_name_list]
    product_price_list = [int(x.replace(",", "")) for x in product_price_list]
    product_enroll_list = [str(x) + "-01" for x in product_enroll_list]
    product_enroll_list = [x.replace(".", "-") for x in product_enroll_list]
    rank = range(1, 51)

    db = DBConnect()
    db.insert(date = crawl_date, hour = crawl_time, rank = rank, name = product_name_list, price = product_price_list, release = product_enroll_list, brand = brand_list, clock = product_clock_list, gen = product_gen_list, purpose = product_purpose_list)

main()