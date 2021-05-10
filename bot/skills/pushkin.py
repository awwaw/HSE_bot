import pickle
import random
import re
import time

from nltk.stem.snowball import RussianStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from bot.bot import Skill
from preprocessing import load_lines


class DialoguesBase:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(decode_error="ignore",
                                          max_features=10000,
                                          min_df=2, max_df=15000,
                                          ngram_range=(1, 3))
        self.neigh = NearestNeighbors(n_jobs=-1)
        self.requests: []
        self.responses: []

    def fit(self, requests: str, responses: str):
        self.requests = load_lines(requests)
        self.responses = load_lines(responses)
        self.neigh.fit(self.vectorizer.fit_transform(self.requests))

    def get_candidate(self, request: str, k=1):

        request = self.apply_stemming(request)
        data = self.vectorizer.transform([request])
        neigh_ind = self.neigh.kneighbors(data, n_neighbors=k, return_distance=False)
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
        if message[0] == '@':
            return message.startswith('@pushkin')
        return len(re.sub(r'[^а-яА-ЯёЁ 0-9]', '', message)) > 0.6 * len(message)

    def answer(self, message: str) -> str:
        if message.startswith('@pushkin'):
            message = message[8:].strip()
        return random.choice(self.base.get_candidate(message, 10))