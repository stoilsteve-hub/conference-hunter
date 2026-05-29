from playwright.sync_api import sync_playwright

class BaseSpider:
    def __init__(self, conference_id, conference_name, url, topic="", speaker_url=""):
        self.conference_id = conference_id
        self.conference_name = conference_name
        self.url = url
        self.topic = topic
        self.speaker_url = speaker_url
        self.data_template = {
            "Conference ID": self.conference_id,
            "Conference Name": self.conference_name,
            "Topic": self.topic,
            "Dates": "TBD",
            "Location": "TBD",
            "Speaker First Name": "",
            "Speaker Full Name": "",
            "Speaker Job Title": "",
            "Speaker Company": "",
            "Presentation Title": "",
            "Speaker Summary": "",
            "Speaker Profile": "",
            "Speaker Email": "",
            "Speaker Image URL": "",
            "Speaker LinkedIn": ""
        }

    def extract(self):
        """Must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement extract()")
