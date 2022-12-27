import time
import re
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from pyQA.FUNCTIONS.helper import Checker
from pyQA.logfile import Logclass
import json


class Function:
    def __init__(self, browser):
        self.cities_count = None
        self.site = None
        self.var = None
        self.type_of = None
        self.validate = None
        self.page_range = None
        self.url = None
        self.browser = browser
        with open("Test_data/Check_city_name/config.json", 'r') as f:
            self.data = json.loads(f.read())

    def common(self, url, page_range=0, site=False, city_count=0):
        self.cities_count = city_count
        self.site = site
        if self.site is True:
            self.url = self.data["common"]["live_url"] + url
        else:
            self.url = self.data["common"]["url"] + url
        self.page_range = page_range
        logger = Logclass()
        log = logger.getLogs()
        errors = []
        urls = []
        run = Checker(self.url, self.browser)
        run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
        Element_count = run.count_all("xpath", self.data["common"]["Cities_name"])
        if type(Element_count) == str:
            page_url = run.current_tab_url()
            urls.append(f"{page_url}")
            print(f"No element to check, page is empty.")
            run.end()
            assert True
        else:
            City_name = run.return_all_inner_text("xpath", self.data["common"]["Cities_name"])
            if city_count == 0:
                for i in range(len(City_name)):
                    try:
                        xpath = "//a[normalize-space()='" + City_name[i] + "']"
                        state_page_url = run.current_tab_url()
                        url = run.listToString(state_page_url.split("/")[-2:])
                        run.cookie_click("xpath", xpath)
                    except:
                        print("   ----------   ")
                        Page_url = run.current_tab_url()
                        errors.append(f"Function Error on this page: " + Page_url)
                        # urls.append(f"{Page_url}")
                        print("City Name: ", City_name[i])
                        print("Function Error on this page: ", Page_url)
                    try:
                        inner_page_url = run.current_tab_url()
                        z = run.listToString(inner_page_url.split("/")[-2:])
                        if url not in z:
                            print("   ----------   ")
                            print("City Name: ", City_name[i])
                            print("State page url: ", state_page_url)
                            print("Error page url: ", inner_page_url)
                            urls.append(f"{inner_page_url}")
                            errors.append(f"{City_name[i]}")
                        else:
                            pass
                        run.page_back()
                    except:
                        print("   ----------   ")
                        Page_url = run.current_tab_url()
                        errors.append(f"Function Error on this page: " + Page_url)
                        print("City Name: ", City_name[i])
                        print("Function Error on this page: ", Page_url)
                        run.page_back()
                if not errors:
                    print("No errors found while checking the state name in the city page url")
                    run.end()
                    assert True
                else:
                    log.error("urls:\n{}".format("\n".join(urls)))
                    log.error("errors occurred:\n{}".format("\n".join(errors)))
                    run.end()
                    assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format("\n".join(urls))
            else:
                for i in range(city_count):
                    try:
                        city_xpath = "//a[normalize-space()='" + City_name[i] + "']"
                        state_page_url = run.current_tab_url()
                        url = run.listToString(state_page_url.split("/")[-2:])
                        run.cookie_click("xpath", city_xpath)
                    except:
                        print("   ----------   ")
                        Page_url = run.current_tab_url()
                        errors.append(f"Function Error on this page: " + Page_url)
                        print("City Name: ", City_name[i])
                        print("Function Error on this page: ", Page_url)
                    try:
                        inner_page_url = run.current_tab_url()
                        z = run.listToString(inner_page_url.split("/")[-2:])
                        if url not in z:
                            print("   ----------   ")
                            print("City Name: ", City_name[i])
                            print("State page url: ", state_page_url)
                            print("Error page url: ", inner_page_url)
                            urls.append(f"{inner_page_url}")
                            errors.append(f"{City_name[i]}")
                        else:
                            pass
                        run.page_back()
                    except:
                        print("   ----------   ")
                        Page_url = run.current_tab_url()
                        errors.append(f"Function Error on this page: " + Page_url)
                        print("City Name: ", City_name[i])
                        print("Function Error on this page: ", Page_url)
                        run.page_back()
                if not errors:
                    print("No errors found while checking the state name in the city page url ")
                    run.end()
                    assert True
                else:
                    log.error("urls:\n{}".format("\n".join(urls)))
                    log.error("errors occurred:\n{}".format("\n".join(errors)))
                    run.end()
                    assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format("\n".join(urls))
