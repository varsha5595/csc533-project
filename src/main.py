import os

from src.parser import Parser
from src.skill_desc_scraper import SkillScraper, flag_skill


def main():
    """
    There are two actions being performed here:
    1. SkillScrapper is used to scrape the description of skills on Alexa Marketplace and check for privacy violation
    2. Flag a skill if there are violations wrt to the Privacy Policy of the skill
    :return: Boolean
    True: Skill is flagged for privacy violation
    False: Skill is not flagged for privacy violation
    """
    parser = Parser()
    skill_list = parser.get_skill_list()
    skill_scraper = SkillScraper(skill_list)
    # skill_scraper.scrape_skill_details()

    for file_name in os.listdir("../plaintext_policies"):
        if file_name.endswith('.txt'):
            skillID = os.path.splitext(file_name)[0]
            flag_status = flag_skill(skillID)
            print("Skill " + skillID + " is violating the privacy policy: " + str(flag_status))

    return


if __name__ == "__main__":
    main()
