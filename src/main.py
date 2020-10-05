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

    # TODO Check privacy policies of all the skills in skill_list
    flag_status = flag_skill('B07KWT2RLP')
    print("Skill 'Loud Bird' is violating the privacy policy: " + str(flag_status))

    return flag_status


if __name__ == "__main__":
    main()
