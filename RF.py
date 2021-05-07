from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import numpy as np


class Classifier:
    def __init__(self, n_estimators: int = 100, max_depth: int = 5, min_samples_split: int = 2,
                 min_samples_leaf: int = 1):
        self.rf = RandomForestClassifier(n_estimators, max_depth, min_samples_split,
                    min_samples_leaf, criterion='entropy')
        self.text = []
        self.X = []
        self.y = []
        self.fitted = False

    def prepare_data(self, filename):
        file = open(filename, 'r', encoding='utf-8')
        first = []
        next = []
        target = []
        cur_dialogue = []
        dialogues = []

        text = []
        SIZE = 3 * 10**5

        for line in file.readlines()[:SIZE]:
            if line != '\n':
                cur_dialogue.append(line[1:-1])
                text.append(line[1:-1])
            else:
                # print(cur_dialogue)
                for i in range(len(cur_dialogue) - 1):
                    first.append(cur_dialogue[i])
                    next.append(cur_dialogue[i + 1])
                    target.append(1)
                dialogues.append(cur_dialogue)
                cur_dialogue.clear()

        f = list(np.random.permutation(np.array(first)))
        first += f
        next += next
        target += [0 for i in range(len(f))]

        vectorizer = TfidfVectorizer(max_features=1000)
        vectorizer.fit(text)
        res_repl = vectorizer.transform(first)
        res_answ = vectorizer.transform(next)

        print(res_repl.shape, res_answ.shape, np.array(target).shape)
        self.X = np.concatenate([res_repl.toarray(), res_answ.toarray()], axis=1)
        self.y = np.array(target)

    def fit(self):
        self.rf.fit(self.X, self.y)
        self.fitted = True

    def predict(self, X: np.ndarray) -> np.ndarray:
        if not self.fitted:
            print("BRUH")
            return np.array([])
        else:
            return self.rf.predict(X)

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        if not self.fitted:
            print("BRUH")
            return np.array([])
        else:
            return self.rf.predict_proba(X)









