from playwright.sync_api import sync_playwright

class BaseSpider:
    def __init__(self, conference_id, conference_name, url):
        self.conference_id = conference_id
        self.conference_name = conference_name
        self.url = url
        self.data_template = {
            "Conference ID": self.conference_id,
            "Conference Name": self.conference_name,
            "Topic": "TBD",
            "Dates": "TBD",
            "Location": "TBD",
            "Speaker First Name": "",
            "Speaker Full Name": "",
            "Speaker Job Title": "",
            "Speaker Company": "",
            "Speaker Summary": "",
            "Speaker Profile": "",
            "Speaker LinkedIn": ""
        }
        
    def extract(self):
        # This will be overridden by subclasses
        return []
