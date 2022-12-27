from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from pyQA.FUNCTIONS.helper import Checker
from pyQA.logfile import Logclass
import json


class Function:
    def __init__(self, browser):
        self.site = None
        self.var = None
        self.type_of = None
        self.validate = None
        self.page_range = None
        self.url = None
        self.browser = browser
        with open("Test_data/City_check_data/config.json", 'r') as f:
            self.data = json.loads(f.read())

    def common(self, url, validate=None, type_of=None, page_range=0, site=False):
        self.site = site
        if self.site is True:
            self.url = self.data["common"]["live_url"] + url
        else:
            self.url = self.data["common"]["url"] + url
        self.page_range = page_range
        self.validate = validate
        self.type_of = type_of
        logger = Logclass()
        log = logger.getLogs()
        errors = []
        urls = []
        run = Checker(self.url, self.browser)
        run.maximize_window()
        run.cookie_click("xpath", self.data["common"]["cookie_click_2"])

        run.display_url()

        if self.page_range == 0:
            while True:
                print()
                error_page_url = run.current_tab_url()
                var = 0
                x = run.count_all("xpath", self.data["common"]["single_page_listing_count"])
                if type(x) == str:
                    page_url = run.current_tab_url()
                    urls.append(f"{page_url}")
                    print(f"No element to check, page is empty.")
                    break
                for a in range(x):
                    c = run.return_text_nth(self.data["common"]["listing_name"], "text", a)
                    c = c.split("\n")
                    c = ' '.join(c)
                    run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    current_url = run.current_tab_url()
                    if self.validate not in c:
                        if self.validate not in c and var == 0:
                            print(f"Page url: {error_page_url}")
                            var += 1
                        if self.validate not in c :
                            print(f"{c}")
                            # urls.append(f"{current_url}")
                            # print(c)
                            errors.append(f"{c}")
                    else:
                        pass
                driver = run.get_driver()
                try:
                    run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    if driver.find_element(By.XPATH, self.data["common"]["page_forward"]):
                        run.button("xpath", self.data["common"]["page_forward"])
                except NoSuchElementException:
                    print("No next page button to click, exiting.....")
                    break
            if not errors:
                run.end()
                assert True
            else:
                log.error("urls:\n{}".format("\n".join(urls)))
                log.error("errors occurred:\n{}".format("\n".join(errors)))
                run.end()
                assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format(
                    "\n".join(urls))
        else:
            while True:
                print()
                error_page_url = run.current_tab_url()
                var = 0
                for a in range(self.page_range):
                    c = run.return_text_nth(self.data["common"]["listing_name"], "text", a)
                    c = c.split("\n")
                    c = ' '.join(c)
                    current_url = run.current_tab_url()
                    if self.validate not in c:
                        if self.validate not in c and var == 0:
                            print(f"Page url: {error_page_url}")
                            var += 1
                        if self.validate not in c:
                            print(f"{c}")
                            # urls.append(f"{current_url}")
                            errors.append(f"{c}")
                    else:
                        pass
                driver = run.get_driver()
                try:
                    run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    if driver.find_element(By.XPATH, self.data["common"]["page_forward"]):
                        run.button("xpath", self.data["common"]["page_forward"])
                except NoSuchElementException:
                    print("No next page button to click, exiting.....")
                    break
            if not errors:
                run.end()
                assert True
            else:
                log.error("urls:\n{}".format("\n".join(urls)))
                log.error("errors occurred:\n{}".format("\n".join(errors)))
                run.end()
                assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format(
                    "\n".join(urls))