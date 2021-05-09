from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score
import random
import numpy as np


class Classifier:
    def __init__(self, n_estimators: int = 100, max_depth: int = 5, min_samples_split: int = 2,
                 min_samples_leaf: int = 2):
        self.rf = RandomForestClassifier(n_estimators, max_depth=max_depth)
            # , max_depth, min_samples_split,
            #         min_samples_leaf, criterion='entropy')
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
        SIZE = 10 * 10**4

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

        vectorizer = TfidfVectorizer(max_features=200)
        vectorizer.fit(text)
        res_repl = vectorizer.transform(first)
        res_answ = vectorizer.transform(next)

        print(res_repl.shape, res_answ.shape, np.array(target).shape)
        self.X = np.concatenate([res_repl.toarray(), res_answ.toarray()], axis=1)
        self.y = np.array(target)
        XY = np.random.permutation(range(len(self.X)))
        _x = self.X
        _y = self.y
        self.X = []
        self.y = []
        for i in range(len(XY)):
            self.X.append(_x[i])
            self.y.append(_y[i])
        self.X = np.array(self.X)
        self.y = np.array(self.y)

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

    def test(self):
        X_train, X_test, y_train, y_test = train_test_split(self.X, self.y, test_size=0.3, random_state=42)
        self.rf.fit(X_train, y_train)
        cross_val_mean = cross_val_score(self.rf, self.X, self.y, cv=5).mean()
        accuracy = accuracy_score(y_test, self.rf.predict(X_test))
        print(f"Cross validation score - {cross_val_mean}")
        print(f"Accuracy score - {accuracy}")
        print(accuracy_score(y_train, self.rf.predict(X_train)))









