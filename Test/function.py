import time
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
        with open("Test_data/Filter_Check_data/config.json", 'r') as f:
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
        try :
            run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
        except NoSuchElementException:
            pass
        # try:
        #     run.shift_to_frame("xpath", self.data["common"]["iframe"])  # shifts to the given iframe
        #     run.explicit_wait(100, "element_to_be_clickable", "xpath", self.data["common"][
        #         "furniture_costs_menu"])  # checks if the button is ready to be clickable max limit is 15sec
        #     run.button("xpath", self.data["common"]["furniture_costs_menu"])  # clicks the button an opens the menu
        #     run.explicit_wait(100, "element_to_be_clickable", "xpath", self.data["common"][
        #         "iframe_close"])  # checks is close button is ready to be clickable max timeout 15 sec
        #     run.button("xpath", self.data["common"]["iframe_close"])  # closes the menu
        #     run.leave_frame()  # leaves the iframe, shifts to the main html
        # except NoSuchElementException:
        #     pass
        if self.type_of == "Price":
            pricing_var = run.return_text("xpath", self.data["common"]["read_price_condition"])
            a = pricing_var.partition('$')[-1].split()
            Min_price = list([val for val in a[0] if val.isnumeric()])## Remove all the charchters excpet the numbers
            var1 = "".join(Min_price)
            Max_Price = list([val for val in a[2] if val.isnumeric()])## Remove all the charchters excpet the numbers
            var2 = "".join(Max_Price)
            num1 = int(var1)
            num2 = int(var2)

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
                    run.increasing_order_click(self.data["common"]["single_listing_click"], "click", a)
                    c = run.return_text_nth(self.data["common"]["listing_name"], "text", a)
                    c = c.split("\n")
                    c = ' '.join(c)
                    run.childscreen()
                    try:
                        element_check = run.return_is_visible("xpath",self.data["common"]["page_forward"])
                        if element_check:
                            pass
                            run.closewindow()
                            run.homescreen()
                        else:
                            # run.increasing_order_click(self.data["common"]["single_listing_click"], "click", a) When listings will open on same tab it requires here.
                            # try:
                            #     run.shift_to_frame("xpath", self.data["common"]["iframe"])  # shifts to the given iframe
                            #     run.explicit_wait(100, "element_to_be_clickable", "xpath", self.data["common"][
                            #         "furniture_costs_menu"])  # checks if the button is ready to be clickable max limit is 15sec
                            #     run.button("xpath",
                            #                self.data["common"]["furniture_costs_menu"])  # clicks the button an opens the menu
                            #     run.explicit_wait(100, "element_to_be_clickable", "xpath", self.data["common"][
                            #         "iframe_close"])  # checks is close button is ready to be clickable max timeout 100 sec
                            #     run.button("xpath", self.data["common"]["iframe_close"])  # closes the menu
                            #     run.leave_frame()  # leaves the iframe, shifts to the main html
                            # except NoSuchElementException:
                            #     pass
                            current_url = run.current_tab_url()
                            run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                            if self.type_of == "Amenities":
                                z = run.return_all_inner_text("xpath", self.data["common"]["read_category"])
                            elif self.type_of == "Price":
                                z = run.return_all_inner_text("xpath", self.data["common"]["validate_price"])
                                z = run.listToString(z)
                                z = z.split("\n")
                                listing_price = list([val for val in z[0] if val.isnumeric()])
                                z = "".join(listing_price) ## Remove all the charchters excpet the numbers
                                z = int(z)
                                if num2 == 3500:
                                    if z >= 3500:
                                        pass  # true
                                    if z < num1 and var == 0:
                                        print(f"Page url: {error_page_url}")
                                        var += 1
                                    if z < num1:
                                        print(f"{current_url}")
                                        urls.append(f"{current_url}")
                                        errors.append(f"{c}")
                                elif num1 <= z <= num2:
                                    pass  # true
                                else:
                                    if var == 0:  ## Added for printing the page number before the error
                                        print(error_page_url)
                                        var += 1
                                    print(f"{current_url}")
                                    urls.append(f"{current_url}")
                                    errors.append(f"{c}")
                            else:
                                z = run.return_all_inner_text("xpath", self.data["common"]["listing_top"])
                            if type_of != "Price":
                                if self.validate not in z and var == 0:
                                    print(error_page_url)
                                    var += 1
                                if self.validate not in z:
                                    print(f"{current_url}")
                                    # run.take_pic()
                                    urls.append(f"{current_url}")
                                    errors.append(f"{c}")
                            else:
                                pass
                            run.closewindow()
                            run.homescreen()
                            # run.page_back() When  listings will open on same tab it requires here for page back.
                    except NoSuchElementException:
                        print("   -------   ")
                        Page_url = run.current_tab_url()
                        errors.append(f"Function Error on this page: " + Page_url)
                        print("Function Error on this page: ", Page_url)
                        run.closewindow()
                        run.homescreen()
                driver = run.get_driver()
                try:
                    try:
                        run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    except NoSuchElementException:
                        pass
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
                    run.increasing_order_click(self.data["common"]["single_listing_click"], "click", a)
                    c = run.return_text_nth(self.data["common"]["listing_name"], "text", a)
                    c = c.split("\n")
                    c = ' '.join(c)
                    run.childscreen()
                    try:
                        run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    except NoSuchElementException:
                        pass
                    try:
                        element_check = run.return_is_visible("xpath", self.data["common"]["page_forward"])
                        if element_check:
                            print("Page redirected to the listings page")
                            pass
                            run.closewindow()
                            run.homescreen()
                        else:
                            # run.increasing_order_click(self.data["common"]["single_listing_click"], "click", a) When listings will open on same tab it requires here.
                            # try:
                            #     run.shift_to_frame("xpath", self.data["common"]["iframe"])  # shifts to the given iframe
                            #     run.explicit_wait(100, "element_to_be_clickable", "xpath", self.data["common"][
                            #         "furniture_costs_menu"])  # checks if the button is ready to be clickable max limit is 15sec
                            #     run.button("xpath",
                            #                self.data["common"]["furniture_costs_menu"])  # clicks the button an opens the menu
                            #     run.explicit_wait(100, "element_to_be_clickable", "xpath", self.data["common"][
                            #         "iframe_close"])  # checks is close button is ready to be clickable max timeout 100 sec
                            #     run.button("xpath", self.data["common"]["iframe_close"])  # closes the menu
                            #     run.leave_frame()  # leaves the iframe, shifts to the main html
                            # except NoSuchElementException:
                            #     pass
                            current_url = run.current_tab_url()
                            if self.type_of == "Amenities":
                                z = run.return_all_inner_text("xpath", self.data["common"]["read_category"])
                            elif self.type_of == "Price":
                                z = run.return_all_inner_text("xpath", self.data["common"]["validate_price"])
                                z = run.listToString(z)
                                z = z.split("\n")
                                getVals = list([val for val in z[0] if val.isnumeric()])
                                z = "".join(getVals)  ## Remove all the charchters excpet the numbers
                                z = int(z)
                                if num2 == 3500:
                                    if z >= 3500:
                                        pass  # true
                                    if z < num1 and var == 0:
                                        print(f"Page url: {error_page_url}")
                                        var += 1
                                    if z < num1:
                                        print(f"{current_url}")
                                        urls.append(f"{current_url}")
                                        errors.append(f"{c}")
                                elif num1 <= z <= num2:
                                    pass  # true
                                else:
                                    if var == 0:  ## Added for printing the page number before the error
                                        print(error_page_url)
                                        var += 1
                                    print(f"{current_url}")
                                    urls.append(f"{current_url}")
                                    errors.append(f"{c}")
                            else:
                                z = run.return_all_inner_text("xpath", self.data["common"]["listing_top"])
                            if type_of != "Price":
                                if self.validate not in z and var == 0:
                                    print(error_page_url)
                                    var += 1
                                if self.validate not in z:
                                    print(f"{current_url}")
                                    # run.take_pic()
                                    urls.append(f"{current_url}")
                                    errors.append(f"{c}")
                            else:
                                pass
                            run.closewindow()
                            run.homescreen()
                            # run.page_back() When  listings will open on same tab it requires here for page back.
                    except NoSuchElementException:
                        print("   -------   ")
                        Page_url = run.current_tab_url()
                        errors.append(f"Function Error on this page: " + Page_url)
                        print("Function Error on this page: ", Page_url)
                        run.closewindow()
                        run.homescreen()
                driver = run.get_driver()
                try:
                    try:
                        run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    except NoSuchElementException:
                        pass
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
