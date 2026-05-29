
from playwright.sync_api import sync_playwright

class BaseSpider:
    def __init__(self, url, **kwargs):
        self.url = url
        self.kwargs = kwargs
        self.data_template = {
            "Conference ID": kwargs.get("conference_id", "AUTO"),
            "Conference Name": kwargs.get("conference_name", "Unknown"),
            "Topic": "Unknown",
            "Dates": "TBD",
            "Location": "TBD",
            "Speaker First Name": "",
            "Speaker Full Name": "",
            "Speaker Job Title": "",
            "Speaker Company": "",
            "Speaker Summary": "",
            "Speaker Profile": "",
            "Speaker Email": "",
            "Speaker Image URL": "",
            "Speaker LinkedIn": ""
        }

    def extract(self):
        """Must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement extract()")
