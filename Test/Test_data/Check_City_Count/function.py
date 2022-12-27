import time
import re
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
        self.cities_count = None
        self.url = None
        self.browser = browser
        with open("Test_data/Check_City_Count/config.json", 'r') as f:
            self.data = json.loads(f.read())

    def common(self, url, City_count=0, site=False):
        self.site = site
        if self.site is True:
            self.url = self.data["common"]["live_url"] + url
        else:
            self.url = self.data["common"]["url"] + url
        self.cities_count = City_count
        logger = Logclass()
        log = logger.getLogs()
        errors = []
        urls = []
        run = Checker(self.url, self.browser)
        run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
        Cities_count = run.count_all("xpath", self.data["common"]["Cities_name"])
        if type(Cities_count) == str:
            page_url = run.current_tab_url()
            urls.append(f"{page_url}")
            print(f"No element to check, page is empty.")
            run.end()
            assert True
        else:
            City_name = run.return_all_inner_text("xpath",self.data["common"]["Cities_name"])
            if City_count == 0:
                for i in range(len(City_name)):
                        try:
                            state_page_url = run.current_tab_url()
                            main_page_listings_numbers = int(re.search(r'\d+', City_name[i]).group())
                            # listings_numbers = 732587235893
                            xpath = "//a[normalize-space()='"+City_name[i]+"']"
                            run.cookie_click("xpath",xpath)
                        except:
                            print("   -------   ")
                            Page_url = run.current_tab_url()
                            errors.append(f"Function Error on this page: "+Page_url)
                            # urls.append(f"{Page_url}")
                            print("City Name: ", City_name[i])
                            print("Function Error on this page: ",Page_url)
                        try:
                            current_url = run.current_tab_url()
                            try:
                                run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                            except :
                                pass
                            inner_page_listings_numbers = run.return_text("xpath",self.data["common"]["Inner_page_listing_count"])
                            z = int(re.search(r'\d+', inner_page_listings_numbers).group())
                            if main_page_listings_numbers == z:
                                pass
                            else:
                                print("   -------   ")
                                print("City Name: ", City_name[i])
                                print("State page url: ", state_page_url)
                                print("Error page url: ", current_url)
                                print("City page listings count: ", inner_page_listings_numbers)
                                urls.append(f"{current_url}")
                                errors.append(f"{City_name[i]}")
                            run.page_back()
                        except:
                            print("   -------   ")
                            Page_url = run.current_tab_url()
                            errors.append(f"Function Error on this page: "+Page_url)
                            print("City Name: ", City_name[i])
                            print("Function Error on this page: ", Page_url)
                            run.page_back()
                if not errors:
                    print("No errors found while checking the cities count under the states")
                    run.end()
                    assert True

                else:
                    log.error("urls:\n{}".format("\n".join(urls)))
                    log.error("errors occurred:\n{}".format("\n".join(errors)))
                    run.end()
                    assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format("\n".join(urls))
            else:
                for i in range(City_count):
                    try:
                        state_page_url = run.current_tab_url()
                        main_page_listings_numbers = int(re.search(r'\d+', City_name[i]).group())
                        # listings_numbers = 732587235893
                        xpath = "//a[normalize-space()='" + City_name[i] + "']"
                        run.cookie_click("xpath", xpath)
                        current_url = run.current_tab_url()
                        try:
                            run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                        except :
                            pass
                    except:
                        print("   -------   ")
                        Page_url = run.current_tab_url()
                        errors.append(f"Function Error on this page: " + Page_url)
                        print("City Name: ", City_name[i])
                        print("Function Error on this page: ", Page_url)
                    try:
                        inner_page_listings_numbers = run.return_text("xpath",self.data["common"]["Inner_page_listing_count"])
                        z = int(re.search(r'\d+', inner_page_listings_numbers).group())
                        if main_page_listings_numbers == z:
                            pass
                        else:
                            print("   -------   ")
                            print("City Name: ", City_name[i])
                            print("State page url: ", state_page_url)
                            print("Error page url: ", current_url)
                            print("City page listings count: ", inner_page_listings_numbers)
                            urls.append(f"{current_url}")
                            errors.append(f"{City_name[i]}")
                        run.page_back()
                    except:
                        print("   -------   ")
                        Page_url = run.current_tab_url()
                        errors.append(f"Function Error on this page: "+ Page_url)
                        print("City Name: ", City_name[i])
                        print("Function Error on this page: ", Page_url)
                        run.page_back()
                if not errors:
                    print("No errors found while checking the cities count under the states")
                    run.end()
                    assert True

                else:
                    log.error("urls:\n{}".format("\n".join(urls)))
                    log.error("errors occurred:\n{}".format("\n".join(errors)))
                    run.end()
                    assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format("\n".join(urls))

