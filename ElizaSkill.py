import re
from typing import List
from nltk import tokenize

templates_file = 'doctor.txt'


class Match:
    def __init__(self, tokens: list, indexes: list = []):
        self.indexes = indexes
        self.tokens = tokens

class Template:
    def __init__(self, decomposition: List[str],
                 substitution: List[List[str]] = None):
        self.decomposition = decomposition
        self.substitution = substitution if substitution else []

    def apply(self, sentence: List[str], template: List[str], ind: List[int]):
        ind += [len(sentence)]
        ans = []
        i = 0
        for el in template:
            if not el.isnumeric():
                ans.append(el)
            else:
                ans += sentence[ind[i]:ind[i + 1]]
                i += 1
        return ans

    def __match(self, sentence: List[str], cur_i: int,
              cur_j: int, begins: List[int]) -> List[Match]:
        if (len(self.decomposition) - cur_i) * (len(sentence) - cur_j) == 0:
            if (len(self.decomposition) - cur_i) + (len(sentence) - cur_j) == 0:
                return [Match(sentence, begins)]
            else:
                return []
        if self.decomposition[cur_i].isdigit():
            cur = int(self.decomposition[cur_i])
            if cur > 0:
                if cur_j + cur <= len(sentence):
                    return self.__match(sentence, cur_i + 1, cur_j + cur, begins + [cur_j])
                return []
            else:
                list_results = []
                for k in range(len(sentence) - cur_j):
                    list_results += self.__match(sentence, cur_i + 1, cur_j + k, begins + [cur_j])
                return list_results
        else:
            if sentence[cur_j] == self.decomposition[cur_i]:
                return self.__match(sentence, cur_i + 1, cur_j + 1, begins + [cur_j])
            return []

    def match(self, sentence: List[str]) -> List[Match]:
        return self.__match(sentence, 0, 0, [])

      
class Rule:
    def __init__(self, keyword: str, priority: int = 0,
                 templates: List[Template] = None):
        self.keyword = keyword
        self.priority = priority
        self.templates = templates if templates else []


class ElizaSkill:
    def __init__(self, script_p: str):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pre = {}
        self.post = {}
        self.synonyms = {}
        self.rules = {}
        # self.load_data(script_p)

    #  TODO
    def match(self, message: str) -> bool:
        return True

    #  TODO
    def answer(self, message: str) -> str:
        return ":("

    def load_data(self, script_p: str):
        current_rule = None
        current_template = None
        with open(script_p, 'r') as file:
            for line in file.readlines():
                s = line.strip().replace('\n', '')
                s = re.sub(r'\s+', ' ', line)  # убрать лишние пробелы
                s_type, s = s.split(': ', maxsplit=1)

                if s_type == 'initial':
                    self.initials.append(s)
                elif s_type == 'final':
                    self.finals.append(s)
                elif s_type == 'quit':
                    self.quits.append(s)
                elif s_type == 'pre':
                    token, substitution = s.split(maxsplit=1)
                    self.pre[token] = substitution
                elif s_type == 'post':
                    token, substitution = s.split(maxsplit=1)
                    self.post[token] = substitution
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
                    current_template = Template(self.split_to_tokens(s))
                    current_rule.templates.append(current_template)
                elif s_type == 'reasmb':
                    current_template.substitution.append(s.split())

    def split_to_sent(self, text: str) -> List[str]:
        return tokenize.sent_tokenize(text)

   def split_to_tokens(self, sentences: str) -> List[List[str]]:
        punctuations = '''!()-[]{};:\,<>./?@#$%^&*_~'''
        tokenized_text = self.split_to_sent(sentences)
        words = []
        for sent in tokenized_text:
            no_punct_sent = ""
            for char in sent:
                if char not in punctuations:
                    no_punct_sent = no_punct_sent + char
            words.append(no_punct_sent.split())
        return words

    def preprocess(self, text: str) -> List[List[str]]:
        tokens = [self.split_to_tokens(sentence)
                  for sentence in self.split_to_sent(text)]
        for sentence in tokens:
            for i in range(len(sentence)):
                token = sentence[i].lower()
                token = self.pre.get(token, default=token)
                sentence[i] = token
        return tokens

    def find_keywords(self, tokens: List[str]) -> List[Rule]:
        rules = []
        for token in tokens:
            token = self.synonyms.get(token, default=token)
            if token in self.rules:
                rules.append(self.rules[token])
        return rules

    def match_templates(self):
        pass

    def postprocess(self, tokens):
        new_tokens = tokens
        index = 0
        for token in tokens:
            if token in self.post.keys():
                new_tokens[index] = self.post[token]
            index += 1
        new_phrase = []
        for x in new_tokens:
            if isinstance(x, list):
                for i in x:
                    new_phrase.append(i)
            else:
                new_phrase.append(x)
        answer = " ".join(map(str, new_phrase))
        return answer
