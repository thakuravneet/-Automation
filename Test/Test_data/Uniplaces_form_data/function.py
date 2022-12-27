import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from pyQA.FUNCTIONS.helper import Checker
from pyQA.logfile import Logclass
import json
import datetime


class Function:
    def __init__(self, browser):
        self.site = None
        self.var = None
        self.type_of = None
        self.validate = None
        self.page_range = None
        self.url = None
        self.page_number = None
        self.browser = browser
        with open("Test_data/Uniplaces_form_data/config.json", 'r') as f:
            self.data = json.loads(f.read())

    def common(self, url, validate=None, type_of=None, page_range=0, site=False, page_number=0):
        self.site = site
        if self.site is True:
            self.url = self.data["common"]["live_url"] + url
        else:
            self.url = self.data["common"]["url"] + url
        self.page_range = page_range
        self.validate = validate
        self.type_of = type_of
        self.page_number= page_number
        logger = Logclass()
        log = logger.getLogs()
        errors = []
        urls = []
        current_time = datetime.datetime.now()
        current_day = (current_time.day)
        month = 0
        run = Checker(self.url, self.browser)
        run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
        run.display_url()

        if self.page_range == 0 and self.page_number == 0:
            while True:
                print("-----")
                error_page_url = run.current_tab_url()
                var = 0
                x = run.count_all("xpath", self.data["common"]["single_page_listing_count"])
                if type(x) == str:
                    page_url = run.current_tab_url()
                    urls.append(f"{page_url}")
                    # print(error_page_url)
                    # print(x)
                    print(f"No element to check, page is empty.")
                    break
                for a in range(x):
                    run.increasing_order_click(self.data["common"]["single_listing_click"], "click", a)
                    c = run.return_text_nth(self.data["common"]["listing_name"], "text", a)
                    c = c.split("\n")
                    c = ' '.join(c)
                    run.childscreen()
                    run.set_window_size(1920, 1024)
                    current_url = run.current_tab_url()
                    run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    s = run.return_all_inner_text("xpath",self.data["common"]["check_available_now_in_Listing_Highlights"])
                    if "Available Now" in s:
                        current_year = (current_time.year + 1)
                        next_year = (current_time.year + 2)
                        current_day = 20
                    else:
                        P = run.return_text("xpath", self.data["common"]["Move_in_Date"])
                        t = P.partition(':')[-1].split()
                        year = int(t[2])
                        current_year = (year + 1)
                        next_year = (year + 2)

                    ### First input field started from here
                    run.cookie_click("xpath", self.data["common"]["First_input_click"])
                    run.cookie_click("xpath", self.data["common"]["Year_Click_and_Input"])
                    run.input("xpath", self.data["common"]["Year_Click_and_Input"], current_year)
                    # run.cookie_click ("xpath",self.data["common"]["Month_Selection"])
                    run.static_dropdown("xpath", self.data["common"]["Month_Selection"], "index", str(month))
                    if month == 0:
                        month_name = "January"
                    else:
                        print("Not able to select the Month_Name")
                    run.cookie_click("xpath", "//span[@aria-label='" +month_name+ " " +str(current_day)+ ", "+str(current_year)+"']")  ### Date selection
                    print(current_day)

                    #### Second input field started from here
                    run.cookie_click("xpath", self.data["common"]["Second_Input_Click"])
                    run.cookie_click("xpath", self.data["common"]["Year_Click_and_Input"])
                    run.input("xpath", self.data["common"]["Year_Click_and_Input"], next_year)
                    run.static_dropdown("xpath", self.data["common"]["Month_Selection"], "index", str(month))
                    run.cookie_click("xpath","//div[@class='flatpickr-calendar animate open arrowTop arrowLeft']//span[@aria-label='" + month_name + " " + str(current_day) + ", " + str(next_year) + "']")  ### Date selection

                    ### Guest field started(commented yet no need)
                    # run.cookie_click("xpath",self.data["common"]["Guest_Field_Input"])
                    # run.input("xpath",self.data["common"]["Guest_Field_Input"],1)

                    ### Button click started
                    run.button("xpath", self.data["common"]["Book_Now_button_click"])
                    a = run.return_is_visible("xpath", self.data["common"]["Message_after_redirection"])
                    error_message = run.return_is_visible("xpath", self.data["common"]["Error_message"])
                    # clickable = run.return_is_clickable("xpath","//body/div[@class='wrapper']/div[@class='porpertyDetails-sec']/div[@class='container']/div[@class='porpertyDetails-slider']/div[@class='row']/div[@id='propertyDetailsSideBar']/div[@id='contactLandlordFrame']/div[@class='info contactLandlordContainer w-100']/form[@class='uniplaces-book-form']/div[@id='contactLandlordButtonContainer']/button[1]")
                    if a:
                        z = run.return_all_inner_text("xpath", self.data["common"]["Message_after_redirection"])
                    elif error_message:
                        z = run.return_all_inner_text("xpath", self.data["common"]["Error_message"])
                    else:
                        print("Not able to find the error please check the code")
                    if validate not in z:
                        if validate not in z and var == 0:
                            print(error_page_url)
                            var += 1
                        if validate not in z:
                            self.browser.save_screenshot('./Screenshots/' + str(c) + '.png')
                            print(f"{current_url}")
                            urls.append(f"{current_url}")
                            errors.append(f"{c}")
                    else:
                        time.sleep(5)
                        run.closewindow()
                        run.childscreen()
                        pass
                    run.closewindow()
                    run.homescreen()
                # driver = run.get_driver()
                # try:
                #     run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                #     if driver.find_element(By.XPATH, self.data["common"]["page_forward"]):
                #         run.button("xpath", self.data["common"]["page_forward"])
                # except NoSuchElementException:
                #     print("No next page button to click, exiting.....")
                #     break
                break
            if not errors:
                run.end()
                assert True
            else:
                log.error("urls:\n{}".format("\n".join(urls)))
                log.error("errors occurred:\n{}".format("\n".join(errors)))
                run.end()
                assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format("\n".join(urls))

        elif self.page_range == 0 and self.page_number == 1:
            while True:
                print("-----")
                error_page_url = run.current_tab_url()
                var = 0
                x = run.count_all("xpath", self.data["common"]["single_page_listing_count"])
                if type(x) == str:
                    page_url = run.current_tab_url()
                    urls.append(f"{page_url}")
                    # print(error_page_url)
                    # print(x)
                    print(f"No element to check, page is empty.")
                    break
                for a in range(x):
                    run.increasing_order_click(self.data["common"]["single_listing_click"], "click", a)
                    c = run.return_text_nth(self.data["common"]["listing_name"], "text", a)
                    c = c.split("\n")
                    c = ' '.join(c)
                    run.childscreen()
                    run.set_window_size(1920, 1024)
                    current_url = run.current_tab_url()
                    run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    s = run.return_all_inner_text("xpath",self.data["common"]["check_available_now_in_Listing_Highlights"])
                    if "Available Now" in s:
                        current_year = (current_time.year + 1)
                        next_year = (current_time.year + 2)
                        current_day = 20
                    else:
                        P = run.return_text("xpath", self.data["common"]["Move_in_Date"])
                        t = P.partition(':')[-1].split()
                        year = int(t[2])
                        current_year = (year + 1)
                        next_year = (year + 2)

                    ### First input field started from here
                    run.cookie_click("xpath", self.data["common"]["First_input_click"])
                    run.cookie_click("xpath", self.data["common"]["Year_Click_and_Input"])
                    run.input("xpath", self.data["common"]["Year_Click_and_Input"], current_year)
                    # run.cookie_click ("xpath",self.data["common"]["Month_Selection"])
                    run.static_dropdown("xpath", self.data["common"]["Month_Selection"], "index", str(month))
                    if month == 0:
                        month_name = "January"
                    else:
                        print("Not able to select the Month_Name")
                    run.cookie_click("xpath", "//span[@aria-label='" + month_name + " " + str(current_day) + ", " + str(current_year) + "']")  ### Date selection

                    #### Second input field started from here
                    run.cookie_click("xpath", self.data["common"]["Second_Input_Click"])
                    run.cookie_click("xpath", self.data["common"]["Year_Click_and_Input"])
                    run.input("xpath", self.data["common"]["Year_Click_and_Input"], next_year)
                    run.static_dropdown("xpath", self.data["common"]["Month_Selection"], "index", str(month))
                    run.cookie_click("xpath","//div[@class='flatpickr-calendar animate open arrowTop arrowLeft']//span[@aria-label='" + month_name + " " + str(current_day) + ", " + str(next_year) + "']")  ### Date selection

                    ### Guest field started(commented yet no need)
                    # run.cookie_click("xpath",self.data["common"]["Guest_Field_Input"])
                    # run.input("xpath",self.data["common"]["Guest_Field_Input"],1)

                    ### Button click started
                    run.button("xpath", self.data["common"]["Book_Now_button_click"])
                    a = run.return_is_visible("xpath", self.data["common"]["Message_after_redirection"])
                    error_message = run.return_is_visible("xpath", self.data["common"]["Error_message"])
                    # clickable = run.return_is_clickable("xpath","//body/div[@class='wrapper']/div[@class='porpertyDetails-sec']/div[@class='container']/div[@class='porpertyDetails-slider']/div[@class='row']/div[@id='propertyDetailsSideBar']/div[@id='contactLandlordFrame']/div[@class='info contactLandlordContainer w-100']/form[@class='uniplaces-book-form']/div[@id='contactLandlordButtonContainer']/button[1]")
                    if a:
                        z = run.return_all_inner_text("xpath", self.data["common"]["Message_after_redirection"])
                    elif error_message:
                        z = run.return_all_inner_text("xpath", self.data["common"]["Error_message"])
                    else:
                        print("Not able to find the error please check the code")
                    if validate not in z:
                        if validate not in z and var == 0:
                            print(error_page_url)
                            var += 1
                        if validate not in z:
                            self.browser.save_screenshot('./Screenshots/' + str(c) + '.png')
                            print(f"{current_url}")
                            urls.append(f"{current_url}")
                            errors.append(f"{c}")
                    else:
                        time.sleep(5)
                        run.closewindow()
                        run.childscreen()
                        pass
                    run.closewindow()
                    run.homescreen()
                break
                # driver = run.get_driver()
                # try:
                #     run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                #     if driver.find_element(By.XPATH, self.data["common"]["page_forward"]):
                #         run.button("xpath", self.data["common"]["page_forward"])
                # except NoSuchElementException:
                #     print("No next page button to click, exiting.....")
                #     break
            if not errors:
                run.end()
                assert True
            else:
                log.error("urls:\n{}".format("\n".join(urls)))
                log.error("errors occurred:\n{}".format("\n".join(errors)))
                run.end()
                assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format("\n".join(urls))

        elif self.page_range == 1 and self.page_number == 1:
            while True:
                print("-----")
                error_page_url = run.current_tab_url()
                var = 0
                for a in range(self.page_range):
                    run.increasing_order_click(self.data["common"]["single_listing_click"], "click", a)
                    c = run.return_text_nth(self.data["common"]["listing_name"], "text", a)
                    c = c.split("\n")
                    c = ' '.join(c)
                    run.childscreen()
                    run.set_window_size(1920, 1024)
                    current_url = run.current_tab_url()
                    run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    s = run.return_all_inner_text("xpath",self.data["common"]["check_available_now_in_Listing_Highlights"])
                    if "Available Now" in s:
                        current_year = (current_time.year + 1)
                        next_year = (current_time.year + 2)
                        current_day = 20
                    else:
                        P = run.return_text("xpath", self.data["common"]["Move_in_Date"])
                        t = P.partition(':')[-1].split()
                        year = int(t[2])
                        current_year = (year + 1)
                        next_year = (year + 2)

                    ### First input field started from here
                    run.cookie_click("xpath", self.data["common"]["First_input_click"])
                    run.cookie_click("xpath", self.data["common"]["Year_Click_and_Input"])
                    run.input("xpath", self.data["common"]["Year_Click_and_Input"], current_year)
                    # run.cookie_click ("xpath",self.data["common"]["Month_Selection"])
                    run.static_dropdown("xpath", self.data["common"]["Month_Selection"], "index", str(month))
                    if month == 0:
                        month_name = "January"
                    else:
                        print("Not able to select the Month_Name")
                    run.cookie_click("xpath", "//span[@aria-label='" + month_name + " " + str(current_day) + ", " + str(current_year) + "']")  ### Date selection

                    #### Second input field started from here
                    run.cookie_click("xpath", self.data["common"]["Second_Input_Click"])
                    run.cookie_click("xpath", self.data["common"]["Year_Click_and_Input"])
                    run.input("xpath", self.data["common"]["Year_Click_and_Input"], next_year)
                    run.static_dropdown("xpath", self.data["common"]["Month_Selection"], "index", str(month))
                    run.cookie_click("xpath","//div[@class='flatpickr-calendar animate open arrowTop arrowLeft']//span[@aria-label='" + month_name + " " + str(current_day) + ", " + str(next_year) + "']")  ### Date selection

                    ### Guest field started(commented yet no need)
                    # run.cookie_click("xpath",self.data["common"]["Guest_Field_Input"])
                    # run.input("xpath",self.data["common"]["Guest_Field_Input"],1)

                    ### Button click started
                    run.button("xpath", self.data["common"]["Book_Now_button_click"])
                    a = run.return_is_visible("xpath", self.data["common"]["Message_after_redirection"])
                    error_message = run.return_is_visible("xpath", self.data["common"]["Error_message"])
                    # clickable = run.return_is_clickable("xpath","//body/div[@class='wrapper']/div[@class='porpertyDetails-sec']/div[@class='container']/div[@class='porpertyDetails-slider']/div[@class='row']/div[@id='propertyDetailsSideBar']/div[@id='contactLandlordFrame']/div[@class='info contactLandlordContainer w-100']/form[@class='uniplaces-book-form']/div[@id='contactLandlordButtonContainer']/button[1]")
                    if a:
                        z = run.return_all_inner_text("xpath", self.data["common"]["Message_after_redirection"])
                    elif error_message:
                        z = run.return_all_inner_text("xpath", self.data["common"]["Error_message"])
                    else:
                        print("Not able to find the error please check the code")
                    if validate not in z:
                        if validate not in z and var == 0:
                            print(error_page_url)
                            var += 1
                        if validate not in z:
                            self.browser.save_screenshot('./Screenshots/' + str(c) + '.png')
                            print(f"{current_url}")
                            urls.append(f"{current_url}")
                            errors.append(f"{c}")
                    else:
                        time.sleep(5)
                        run.closewindow()
                        run.childscreen()
                        pass
                    run.closewindow()
                    run.homescreen()
                break
            if not errors:
                run.end()
                assert True
            else:
                log.error("urls:\n{}".format("\n".join(urls)))
                log.error("errors occurred:\n{}".format("\n".join(errors)))
                run.end()
                assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format("\n".join(urls))

        else:
            while True:
                print("-----")
                error_page_url = run.current_tab_url()
                var = 0
                for a in range(self.page_range):
                    run.increasing_order_click(self.data["common"]["single_listing_click"], "click", a)
                    c = run.return_text_nth(self.data["common"]["listing_name"], "text", a)
                    c = c.split("\n")
                    c = ' '.join(c)
                    run.childscreen()
                    run.set_window_size(1920,1024)
                    current_url = run.current_tab_url()
                    run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                    s = run.return_all_inner_text("xpath", self.data["common"]["check_available_now_in_Listing_Highlights"])
                    if "Available Now" in s:
                        current_year = (current_time.year + 1)
                        next_year = (current_time.year + 2)
                        current_day = 20
                    else:
                        P = run.return_text("xpath", self.data["common"]["Move_in_Date"])
                        t = P.partition(':')[-1].split()
                        year = int(t[2])
                        current_year = (year + 1)
                        next_year = (year + 2)

                    ### First input field started from here
                    run.cookie_click("xpath", self.data["common"]["First_input_click"])
                    run.cookie_click("xpath",self.data["common"]["Year_Click_and_Input"])
                    run.input("xpath",self.data["common"]["Year_Click_and_Input"],current_year)
                    # run.cookie_click ("xpath",self.data["common"]["Month_Selection"])
                    run.static_dropdown("xpath",self.data["common"]["Month_Selection"],"index", str(month))
                    if month == 0:
                        month_name = "January"
                    else:
                        print("Not able to select the Month_Name")
                    run.cookie_click("xpath", "//span[@aria-label='" +month_name+ " " +str(current_day)+ ", " +str(current_year)+ "']")  ### Date selection

                    #### Second input field started from here
                    run.cookie_click("xpath",self.data["common"]["Second_Input_Click"])
                    run.cookie_click("xpath",self.data["common"]["Year_Click_and_Input"])
                    run.input("xpath",self.data["common"]["Year_Click_and_Input"],next_year)
                    run.static_dropdown("xpath",self.data["common"]["Month_Selection"],"index", str(month))
                    run.cookie_click("xpath", "//div[@class='flatpickr-calendar animate open arrowTop arrowLeft']//span[@aria-label='" +month_name+ " " +str(current_day)+ ", " +str(next_year)+ "']")### Date selection

                    ### Guest field started(commented yet no need)
                    # run.cookie_click("xpath",self.data["common"]["Guest_Field_Input"])
                    # run.input("xpath",self.data["common"]["Guest_Field_Input"],1)

                    ### Button click started
                    run.button("xpath",self.data["common"]["Book_Now_button_click"])
                    a = run.return_is_visible("xpath", self.data["common"]["Message_after_redirection"])
                    error_message = run.return_is_visible("xpath",self.data["common"]["Error_message"])
                    # clickable = run.return_is_clickable("xpath","//body/div[@class='wrapper']/div[@class='porpertyDetails-sec']/div[@class='container']/div[@class='porpertyDetails-slider']/div[@class='row']/div[@id='propertyDetailsSideBar']/div[@id='contactLandlordFrame']/div[@class='info contactLandlordContainer w-100']/form[@class='uniplaces-book-form']/div[@id='contactLandlordButtonContainer']/button[1]")
                    if a:
                        z = run.return_all_inner_text("xpath", self.data["common"]["Message_after_redirection"])
                    elif error_message:
                        z = run.return_all_inner_text("xpath",self.data["common"]["Error_message"])
                    else:
                        print("Not able to find the error please check the code")
                    if validate not in z:
                        if validate not in z and var == 0:
                            print(error_page_url)
                            var += 1
                        if validate not in z:
                            self.browser.save_screenshot('./Screenshots/'+str(c)+'.png')
                            print(f"{current_url}")
                            urls.append(f"{current_url}")
                            errors.append(f"{c}")
                    else:
                        time.sleep(5)
                        run.closewindow()
                        run.childscreen()
                        pass
                    run.closewindow()
                    run.homescreen()
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
                assert False, "errors occurred:\n{}".format("\n".join(errors)) + "\n" + "urls:\n{}".format("\n".join(urls))