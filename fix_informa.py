from core.engine import Engine

e = Engine()
urls_to_scrape = [
    url for url in e.spider_map.keys() 
    if 'informaconnect.com' in url
]

print(f"Rescraping {len(urls_to_scrape)} Informa URLs to bypass Wayback timeouts...")
e.load_urls(urls_to_scrape)
e.run()
