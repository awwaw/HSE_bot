import re
import random
from typing import List, Dict
from nltk import tokenize

from bot.bot import Skill


class Match:
    def __init__(self, tokens: List[str], indexes: List[int]):
        self.indexes = indexes
        self.tokens = tokens


class Template:
    def __init__(self, decomposition: List[str],
                 substitutions: List[List[str]] = None,
                 synonyms: Dict[str, str] = None):
        self.decomposition = decomposition
        self.substitution = substitutions if substitutions else []
        self.synonyms = synonyms if synonyms else {}

    def apply(self, match: Match, choice=None):
        post_mask = []
        if choice is None:
            choice = random.randint(0, len(self.substitution) - 1)
        begins = match.indexes + [len(match.tokens)]
        answer = []
        for element in self.substitution[choice]:
            if not element.isnumeric():
                answer.append(element)
                post_mask.append(False)
            else:
                i = int(element)
                answer += match.tokens[begins[i]:begins[i + 1]]
                post_mask.extend(True for _ in range(begins[i + 1] - begins[i] + 1))
        return answer, post_mask

    def match(self, sentence: List[str]) -> List[Match]:
        return self.__match(sentence, 0, 0, [])

    def __match(self, sentence: List[str], decomposition_ptr: int,
                sentence_ptr: int, begins: List[int]) -> List[Match]:
        if decomposition_ptr == len(self.decomposition) and sentence_ptr == len(sentence):
            return [Match(sentence, begins)]
        if decomposition_ptr == len(self.decomposition) or sentence_ptr == len(sentence):
            return []
        decomposition_rule = self.decomposition[decomposition_ptr]
        if decomposition_rule.isdigit():
            cur = int(decomposition_rule)
            if cur > 0:
                if sentence_ptr + cur <= len(sentence):
                    return self.__match(sentence, decomposition_ptr + 1,
                                        sentence_ptr + cur, begins + [sentence_ptr])
                return []
            else:
                list_results = []
                for k in range(len(sentence) - sentence_ptr + 1):
                    list_results += self.__match(sentence, decomposition_ptr + 1,
                                                 sentence_ptr + k, begins + [sentence_ptr])
                return list_results
        elif decomposition_rule.startswith('@'):
            if self.synonyms.get(sentence[sentence_ptr], '') == decomposition_rule[1:]:
                return self.__match(sentence, decomposition_ptr + 1,
                                    sentence_ptr + 1, begins + [sentence_ptr])
            return []
        else:
            if sentence[sentence_ptr] == decomposition_rule:
                return self.__match(sentence, decomposition_ptr + 1,
                                    sentence_ptr + 1, begins + [sentence_ptr])
            return []


class Rule:
    def __init__(self, keyword: str, priority: int = 0,
                 templates: List[Template] = None):
        self.keyword = keyword
        self.priority = priority
        self.templates = templates if templates else []

    def find_template(self, decomposition):
        for template in self.templates:
            if template.decomposition == decomposition:
                return template
        return None


class ElizaSkill(Skill):
    def __init__(self, script_p: str = None):
        self.initials: List[str] = []
        self.finals: List[str] = []
        self.quits: List[str] = []
        self.pre: Dict[str, List[str]] = {}
        self.post: Dict[str, List[str]] = {}
        self.synonyms: Dict[str, str] = {}
        self.rules: Dict[str, Rule] = {}

        if script_p is not None:
            self.load_data(script_p)

    def match(self, message: str) -> bool:
        return True

    def answer(self, message: str) -> str:
        sentences = self.preprocess(message)
        sentence = max(sentences, key=len)

        rules = self.find_keywords(sentence)
        rules.sort(reverse=True, key=lambda x: x.priority)

        possible_templates = []

        for rule in rules:
            for template in rule.templates:
                match = template.match(sentence)
                if len(match) != 0:
                    possible_templates.append((template, random.choice(match)))

        if possible_templates:
            random_template = random.choice(possible_templates)
            message, mask = random_template[0].apply(random_template[1])
            response = self.postprocess(message, mask)
            return response

        return 'Я вас не поняла :('

    def load_data(self, script_p: str):
        current_rule = None
        current_template = None
        goto_links = {}
        with open(script_p, 'r') as file:
            for line in file.readlines():
                s = line.strip().replace('\n', '')
                s = re.sub(r'\s+', ' ', s)

                if s == '':
                    break
                s_type, s = s.split(': ', maxsplit=1)

                if s_type == 'initial':
                    self.initials.append(s)
                elif s_type == 'final':
                    self.finals.append(s)
                elif s_type == 'quit':
                    self.quits.append(s)
                elif s_type == 'pre':
                    token, substitution = s.split(maxsplit=1)
                    self.pre[token] = self.split_to_tokens(substitution)
                elif s_type == 'post':
                    token, substitution = s.split(maxsplit=1)
                    self.post[token] = self.split_to_tokens(substitution)
                elif s_type == 'synon':
                    synonyms = s.split()
                    for synonym in synonyms[1:]:
                        self.synonyms[synonym] = synonyms[0]
                elif s_type == 'key':
                    tokens = s.split()
                    priority = 0 if len(tokens) < 2 else int(tokens[1])
                    current_rule = Rule(tokens[0], priority=priority)
                    current_template = None
                    self.rules[current_rule.keyword] = current_rule
                elif s_type == 'decomp':
                    current_template = Template(s.split(), synonyms=self.synonyms)
                    current_rule.templates.append(current_template)
                elif s_type == 'reasmb':
                    tokens = s.split()
                    if tokens[0] == 'goto':
                        goto_links[current_template] = tokens[1]
                    else:
                        current_template.substitution.append(tokens)

    def __handle_goto(self, goto_links: Dict[Template, str]):

        ready_templates = set()

        def __substitute_goto(keyword, template):
            linked = self.rules[keyword].find_template(template.decomposition)
            if not linked:
                linked = self.rules[keyword].find_template(['0'])
            if linked in goto_links and linked not in ready_templates:
                __substitute_goto(goto_links[linked], linked)
            template.substitution.extend(linked.substitution)
            ready_templates.add(template)

        for current_template, current_keyword in goto_links.items():
            if current_template not in ready_templates:
                __substitute_goto(current_keyword, current_template)

    def split_to_sent(self, text: str) -> List[str]:
        return tokenize.sent_tokenize(text)

    def split_to_tokens(self, sentence: str) -> List[str]:
        sentence = re.sub(r'[!()\-\[\]{};:\\,<>./?@#$%^&*_~]', ' ', sentence)
        return sentence.split()

    def preprocess(self, text: str) -> List[List[str]]:
        tokens = [self.split_to_tokens(sentence)
                  for sentence in self.split_to_sent(text)]
        result = []
        for sentence in tokens:
            result.append([])
            for token in sentence:
                token = token.lower()
                result[-1].append(self.pre.get(token[0], token))
        return result

    def find_keywords(self, tokens: List[str]) -> List[Rule]:
        rules = []
        for token in tokens:
            token = self.synonyms.get(token, token)
            if token in self.rules:
                rules.append(self.rules[token])
        return rules

    def postprocess(self, tokens: List[str], post_mask: List[bool]) -> str:
        new_tokens = []
        for el_id, token in enumerate(tokens):
            if token in self.post.keys() and post_mask[el_id]:
                new_tokens.extend(self.post[token])
            else:
                new_tokens.append(token)

        result = ' '.join(new_tokens).capitalize()
        result = re.sub(r'[.!?] *\w', lambda x: x.group().upper(), result)
        if not result[-1].isalpha() and result[-2] == ' ':
            result = result[:-2] + result[-1]

        return result
