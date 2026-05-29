from core.exporter import Exporter

class Engine:
    def __init__(self):
        self.exporter = Exporter()
        self.urls = []

    def load_urls(self, url_list):
        self.urls = url_list
        print(f"Loaded {len(self.urls)} urls to scrape.")

    def run(self):
        print("Engine starting... gonna loop through urls now")
        all_scraped_data = []
        for url in self.urls:
            print(f"Scraping {url}...")
            # Here we will call specific spiders
            # For now just dummy data
            dummy_data = {
                "Conference ID": "123",
                "Conference Name": "Pharma Test Conf",
                "Topic": "Medicine",
                "Dates": "Oct 10-12, 2026",
                "Location": "London, UK",
                "Speaker First Name": "John",
                "Speaker Full Name": "John Doe",
                "Speaker Job Title": "Chief Scientist",
                "Speaker Company": "Big Pharma Inc",
                "Speaker Summary": "He does science",
                "Speaker Profile": "URL here",
                "Speaker LinkedIn": "linkedin.com/in/johndoe"
            }
            all_scraped_data.append(dummy_data)
        
        if all_scraped_data:
            self.exporter.save_data(all_scraped_data)
        print("Engine finished running!")
