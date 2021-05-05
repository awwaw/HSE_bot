class ELIZA:
    """def __init__(self, p):"""

    """def load_data(self, p):"""

    """def split_to_sent(self):"""

    """def split_to_tokens(self):"""

    """def preprocess(self):"""

    def find_keywords(self, sentences_list, keywords):
        for sentence in sentences_list:
            lst = []
            for mas in keywords:
                for word in mas:
                    if word in sentence:
                        lst.append(word)
            print('{0} key word(s) in sentence: {1}'.format(len(lst), ', '.join(lst)))
            print(sentence + "\n")

    """def match_templates(self):"""
