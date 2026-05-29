import os
import requests
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
            "Speaker Image URL": "",
            "Speaker Image Local Path": "",
            "Speaker LinkedIn": ""
        }
        
        # ensure images directory exists
        os.makedirs("images", exist_ok=True)

    def extract(self):
        """Must be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement extract()")
        
    def download_image(self, image_url, speaker_name):
        if not image_url:
            return ""
        try:
            safe_name = "".join([c for c in speaker_name if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(" ", "_").lower()
            if not safe_name:
                safe_name = "unknown"
            filename = f"images/{safe_name}.jpg"
            if os.path.exists(filename):
                return filename
            
            resp = requests.get(image_url, timeout=10)
            if resp.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(resp.content)
                return filename
        except Exception as e:
            print(f"Failed to download image {image_url}: {e}")
        return ""
