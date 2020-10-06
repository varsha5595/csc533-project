import csv


class Parser:

    def __init__(self):
        self.skill_list_file = './skill_list.csv'

    def get_skill_list(self):
        """
        Description: Parses through the CSV file to create a list of Alexa Skills
        :return: List of Alexa SkillIDs
        """
        with open(self.skill_list_file) as skills_csv:
            reader = csv.reader(skills_csv)
            skill_list = list(reader)
        return skill_list[0]

