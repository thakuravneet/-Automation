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
                try:
                    run.cookie_click("xpath", self.data["common"]["cookie_click_2"])
                except NoSuchElementException:
                    pass