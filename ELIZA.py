import re

templates_file = 'doctor.txt'


class Rule:
    def __init__(self, decomp):
        self.decomp = decomp
        self.reasmb = []


class ELIZA:
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pre = {}
        self.post = {}
        self.synonyms = {}
        self.templates = {}

    def load_data(self):
        current_key = ''
        decomp_id = -1
        with open(templates_file, 'r') as file:
            for line in file.readlines():
                s = line.replace('\n', '')
                s = s.strip()

                re.sub("\s\s+", " ", line)  # убрать лишние пробелы

                s_type = s[:s.find(':')]
                s = s[s.find(':') + 2:]

                if s_type == 'initial':
                    self.initials.append(s)
                elif s_type == 'final':
                    self.finals.append(s)
                elif s_type == 'quit':
                    self.quits.append(s)
                elif s_type == 'pre':
                    # s = s.split(' = ')
                    s = s.split()
                    self.pre[s[0]] = s[1]
                elif s_type == 'post':
                    # s = s.split(' = ')
                    s = s.split()
                    self.post[s[0]] = s[1]
                elif s_type == 'synon':
                    # s = s.split(',')
                    s = s.split()
                    for synonym in s[1:]:
                        self.synonyms[synonym] = s[0]
                elif s_type == 'key':
                    current_key = s
                    decomp_id = -1
                    self.templates[s] = []
                elif s_type == 'decomp':
                    decomp_id += 1
                    self.templates[current_key].append(Rule(s))
                elif s_type == 'reasmb':
                    self.templates[current_key][decomp_id].reasmb = s

    def split_to_sent(self):
        pass

    def split_to_tokens(self):
        pass

    def preprocess(self):
        pass

    def find_keywords(self, key_words, tokens):
        for token in tokens:
            lst = []
            if token in key_words.keys():
                lst.append(key_words[token])
            print('{0} key word(s) in sentence: {1}'.format(len(lst), ', '.join(lst)))
            print(token + "\n")

    def match_templates(self):
        pass
