from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, HTTPError
from json import dump

class SkillScraper:

    def __init__(self, skill_list):
        self.skill_list = skill_list
        self.parsed_skills = {}

    def scrape_skills(self):
        for skillID in self.skill_list:
            self.parsed_skills[skillID] = {}

            request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/50.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Connection": "keep-alive" 
            }
            request = Request("https://www.amazon.com/dp/" + skillID, headers=request_headers)
            skill_page = urlopen(request)
            html = skill_page.read().decode("utf-8")
            skill_page.close()
            soup = BeautifulSoup(html, "html.parser")

            self.parsed_skills[skillID] = {
                'skill_name:': soup.select('title')[0].get_text(), 
                'skill_description': soup.select('div > #a2s-description')[0].get_text()
            }

        with open('scraped_skills', 'w+') as f:
            dump(self.parsed_skills, f)
            f.close()

        return 