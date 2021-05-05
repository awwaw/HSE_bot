class ELIZA:

    """def __init__(self, p):"""

    """def load_data(self, p):"""

    """def split_to_sent(self):"""

    """def split_to_tokens(self):"""

    """def preprocess(self):"""

    def find_keywords(self, key_words, tokens):
        for token in tokens:
            lst = []
            if token in key_words.keys():
                lst.append(key_words[token])
            print('{0} key word(s) in sentence: {1}'.format(len(lst), ', '.join(lst)))
            print(token + "\n")

    """def match_templates(self):"""
