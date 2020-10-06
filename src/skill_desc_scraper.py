from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from json import dump
from re import sub
from nltk.util import ngrams


def generate_tokens(privacy_policy):
    """
    :param privacy_policy: privacy policy of the Alexa skill
    Tokenize the privacy policy of an Alexa Skill
    :return: list of words from the privacy policy
    """
    tokens = []
    privacy_policy = open(privacy_policy, encoding="utf-8")
    tokens.append(privacy_policy.read().replace("\n", " "))
    tokens = ("".join(sub(r'[^A-Za-z0-9]+', " ", str(tokens))).lower()).split()

    return tokens


def generate_general_declaration():
    """
    As per the paper, there exists three declaration types:
    collect_info = ['collect', 'gather', 'check'] -> 1
    general_term = ['personal information', 'personal data'] -> 2
    relationship_words = ['such as', 'include'] ->3
    """

    declaration_types = {
        'collect': 1,
        'gather': 1,
        'check': 1,
        'personal information': 2,
        'personal data': 2,
        'such as': 3,
        'include': 3
    }

    general_declaration_trie = Trie()
    general_declaration_trie.insert(declaration_types)

    return general_declaration_trie


def flag_skill(skillID):
    """
    :param skillID: unique ID of the Alexa skill
    Skills are flagged based on two condition:
    1. If the privacy related word is not present in the privacy policy
    2. If the privacy related word is present but not in the right context
    :return: Boolean
    True: Skill is flagged for privacy violation
    False: Skill is not flagged for privacy violation
    """

    # TODO: Take input based on the interaction with the Alexa skill
    privacy_related_words = ['name']
    pp_unigrams = generate_tokens('../plaintext_policies/' + skillID + '.txt')

    presence_check = any(word in pp_unigrams for word in privacy_related_words)

    # Checking for condition 1 if the privacy related word is present in the policy
    if not presence_check:
        return True
    else:
        # Checking for condition 2 if the privacy related word is present but not in the right context
        pp_ngrams = list(ngrams(pp_unigrams, 15))
        general_declaration_trie = generate_general_declaration()

        for privacy_word in privacy_related_words:
            for ngram in pp_ngrams:
                if privacy_word in ngram and general_declaration_trie.search(ngram):
                    return False

        return True


class Trie:
    class Node:
        def __init__(self, value):
            """
            :param value: is a single word
            isPhrase: Boolean
                      True - if the phrase until the node are present in the declaration_types
                      False - if the phrase until the node is not present in the declaration_types
            category: Integer
                      The declaration type the phrase until the word belongs to
            """
            self.value = value
            self.isPhrase = False
            self.children = {}
            self.category = None

    def __init__(self):
        self.root = self.Node(None)

    def insert(self, declaration_types) -> None:
        """
        :param declaration_types: dictionary containing the general declaration type as mentioned in the paper
        :return: a Trie structure of the general declaration types
        """
        for phrase in declaration_types.keys():
            cur = self.root
            for word in phrase.split():
                if word not in cur.children:
                    node = self.Node(word)
                    cur.children[word] = node
                    cur = node
                else:
                    cur = cur.children[word]
                cur.category = declaration_types[word] if word in declaration_types else None
            cur.isPhrase = True

    def search(self, sentence):
        """
        :param sentence: an ngram from the privacy policy
        :return: Boolean
                True - >=2 declaration types are present in the ngram, so right context
                False - >=2 declaration types are not present in the ngram, wrong context
        """
        found_declarations = []

        cur = self.root
        for word in sentence:
            if word not in cur.children:
                continue
            elif cur.children[word].isPhrase:
                found_declarations.append(cur.children[word].category)
                cur = self.root
                if len(set(found_declarations)) >= 2:
                    return True
                continue
            else:
                cur = cur.children[word]

        return False


class SkillScraper:

    def __init__(self, skill_list):
        self.skill_list = skill_list
        self.parsed_skills = {}

    def scrape_skill_details(self):
        """
        Used to scrape the description of skills on Alexa Marketplace and check for privacy violation
        """
        for skillID in self.skill_list:
            self.parsed_skills[skillID] = {}

            request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.2 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/52.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Connection": "keep-alive"
            }
            request = Request("https://www.amazon.com/dp/" + skillID, headers=request_headers)
            skill_page = urlopen(request)
            html = skill_page.read().decode("utf-8")
            skill_page.close()
            soup = BeautifulSoup(html, "html.parser")

            with open(skillID, 'w+') as f1:
                f1.write(soup.get_text())
                f1.close()

            self.parsed_skills[skillID] = {
                'skill_name:': soup.select('title')[0].get_text(),
                'skill_description': soup.select('div > #a2s-description > span')[0].get_text()
            }

        with open('scraped_skills', 'w+') as f:
            dump(self.parsed_skills, f)
            f.close()

        return
