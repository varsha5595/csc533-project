import sys
sys.path.append(".")

from parser import Parser
from skill_desc_scraper import SkillScraper

def main():
    parser = Parser()
    skill_list = parser.get_skill_list()
    skill_scraper = SkillScraper(skill_list)
    skill_scraper.scrape_skills()
    
if __name__ == "__main__":
    main()