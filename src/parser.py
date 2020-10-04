import csv

class Parser:

    def __init__(self):
        self.skill_list_file = 'src/skill_list.csv' 

    def get_skill_list(self):
        '''
        Input: CSV file containing a list of Alexa Skill IDs 
        Description: Parses through the CSV file to create a list of Alexa Skills
        '''
        with open(self.skill_list_file) as skills_csv:
            reader = csv.reader(skills_csv)
            skill_list = list(reader)
        return skill_list[0]
    