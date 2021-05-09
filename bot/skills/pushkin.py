import pickle
import re
import random

from nltk.stem.snowball import RussianStemmer

from bot.bot import Skill
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import time


class DialoguesBase:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(decode_error="ignore", max_features=20)
        self.neigh = NearestNeighbors()
        self.requests: []
        self.responses: []

    def fit(self, requests: str, responses: str):
        start = time.time()
        self.requests = self.load(requests)
        self.responses = self.load(responses)
        self.neigh.fit(self.vectorizer.fit_transform(self.requests))
        end = time.time()
        print(end - start)

    def get_candidate(self, request: str, k=1) -> List[str]:

        neigh_ind = self.neigh.kneighbors(request, n_neighbors=k, return_distance=False)
        result = []
        for ind in neigh_ind[0]:
            result.append(self.responses[ind])
        return result

    def dump(self, dst_path: str):
        with open(dst_path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def apply_stemming(request: str):
        stemmer = RussianStemmer()
        request = re.sub(r'[!()\-\[\]{};:\\,<>./?@#$%^&*_~]', ' ', request).strip().split()
        stemmed = []
        for word in request:
            stemmed.append(stemmer.stem(word))
        return " ".join(stemmed)

    @staticmethod
    def load(src_path: str):
        with open(src_path, 'rb') as f:
            return pickle.load(f)


class PushkinSkill(Skill):
    def __init__(self, data_path):
        self.base = DialoguesBase.load(data_path)

    def match(self, message: str) -> bool:
        return True

    def answer(self, message: str) -> str:
        return random.choice(self.base.get_candidate(message, 5))


db = DialoguesBase()
db.fit("../../stemmed.txt", "../../responses.txt")
db.dump("../../save.tmp")
skill = PushkinSkill("../../save.tmp")
print(skill.answer("Пока, толстуха!"))