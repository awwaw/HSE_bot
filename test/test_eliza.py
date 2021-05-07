from unittest import TestCase
from bot.skills.eliza import ElizaSkill
from bot.skills.eliza import Template, Rule


class TestEliza(TestCase):
    def test_split_to_tokens(self):
        skill = ElizaSkill()
        self.assertEqual(['Hello', 'my', 'dear', 'father', 'How', 'are', 'you'],
                         skill.split_to_tokens('Hello,_my_dear @father!!!! How are you?'))

    def test_preprocess(self):
        skill = ElizaSkill()
        self.assertEqual([['hello', 'my', 'dear', 'father'], ['tell', 'me', 'how', 'was', 'your', 'day']],
                         skill.preprocess("Hello my dear father. Tell me, how was your day?"))

    # def test_find_keyword(self):
    #     skill = ElizaSkill()
    #     rules = Rule
    #     inp = 'Hello,_my_dear @father!!!! How are you?'
    #     inp = skill.preprocess(inp)
    #
    #     self.assertEqual(rules, skill.find_keywords(inp)[0])
