class ELIZA:

    """def __init__(self, keywords):"""

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
