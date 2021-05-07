from unittest import TestCase
from bot.skills.echo import EchoSkill


class TestEchoSkill(TestCase):
    def test_match(self):
        skill = EchoSkill()
        self.assertTrue(skill.match('Some string'))
        self.assertTrue(skill.match('Another string with symbols $$@^!'))

    def test_answer(self):
        skill = EchoSkill()
        self.assertEqual('Some string', skill.answer('Some string'))
        self.assertEqual('Another string with symbols $$@^!',
                         skill.answer('Another string with symbols $$@^!'))
