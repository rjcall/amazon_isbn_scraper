from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from database_functions import push_book, load_json, create_json, add_price
from datetime import date
from time import sleep
from testclear import clear_cache
class Amazon_Scraper:
    def __init__(self, _isbns):
        # put the path to your driver
        self.create_driver()
        self.driver.set_window_size(1024, 768)  # optional
        self.isbns = _isbns
        self.book_dict = load_json()
        self.COOKIES_DICT = {}
        self.myclasses = {}
        self.driver.get("https://amazon.com")
        self.allbooks = []
        self.count = 0

    def isbn(self, num, count):
        book = {}
        try:
            elem = self.driver.find_element_by_xpath("//*[@id='twotabsearchtextbox']")
        except:
            self.driver.get("https://amazon.com")
            elem = self.driver.find_element_by_xpath("//*[@id='twotabsearchtextbox']")

        elem.click()
        elem.clear()
        elem.send_keys(num)
        elem.send_keys(Keys.RETURN)
        url_check = self.driver.current_url

        if '/s/' in url_check:
            try:
                cl = self.driver.find_element_by_xpath("//*[@id='result_0']/div/div/div/div[2]/div[1]/div[1]/a")
                cl.click()
            except:
                try:
                    cl = self.driver.find_element_by_xpath("//*[@id='result_0']/div/div/div/div[2]/div[1]/div[1]/a")
                    cl.click()
                except:
                    print(num + " is not sold on amazon")
                    return

        print(url_check)
        book['title'] = self.get_title()
        book['price'] = self.get_price()
        self.count = 0
        book['isbn'] = num
        book['url'] = self.driver.current_url
        book['date'] = date.today()

        #push_book(book)
        add_price(book, self.book_dict)
        print(book['date'])
        self.allbooks.append(book)
        self.get_cookies()


    def get_title(self):
        book = 'Couldnt find title'
        try:
            book = self.driver.find_element_by_xpath("//*[@id='productTitle']").text
            print(book)
        except Exception:
            pass
        return book



    def get_price(self):
        try:
            book = self.driver.find_element_by_xpath("//*[@id='mediaNoAccordion']/div[1]/div[2]/span[2]").text
            print(book)
            return book
        except Exception as e:
            try:
                book = self.driver.find_element_by_xpath("//*[@id='addToCart']/div[1]/a/h5/div/div[2]/span[2]").text
                print(book)
                return book
            except Exception as g:
                try:
                    book = self.driver.find_element_by_xpath("//*[@id='a-autoid-1-announce']/span[2]").text
                    print(book)
                    return book
                except:
                    try:
                        book = self.driver.find_element_by_xpath("// *[ @ id = 'singleLineOlp'] / span / span").text
                        print(book)
                        return book
                    except:
                        if self.count < 1:
                            self.count+=1
                            self.get_price()
                        else:
                            print("Unable to obtain price")
                        return 'unable to obtain price'
    def create_driver(self):
        # put the path to your driver

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="C:\\Users\\jace\\Documents\\chromedriver_win32\\chromedriver.exe")

    def get_cookies(self):
        cookies_list = self.driver.get_cookies()
        for cookie in cookies_list:
            self.driver.get_cookies()

    def get_all_books(self):
        for x in self.isbns:
            try:
                self.isbn(x, 0)
            except:
                print('Amazon knows im a robot\nClosing driver and trying again')
                clear_cache(self.driver)
                self.isbns(x,0)
        create_json(self.book_dict)



