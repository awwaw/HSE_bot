from unittest import TestCase

from bot.skills.eliza import ElizaSkill


class TestEliza(TestCase):
    def test_split_to_tokens(self):
        skill = ElizaSkill()
        self.assertEqual(
            ['Hello', 'my', 'dear', 'father', 'How', 'are', 'you'],
            skill.split_to_tokens('Hello,_my_dear @father!!!! How are you?'))

    def test_preprocess(self):
        skill = ElizaSkill()
        self.assertEqual(
            [['hello', 'my', 'dear', 'father'],
             ['tell', 'me', 'how', 'was', 'your', 'day']],
            skill.preprocess("Hello my dear father. Tell me, how was your day?"))
