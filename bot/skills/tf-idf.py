from __future__ import annotations
import pickle
import random
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer

from bot.bot import Skill


class DialoguesBase:
    def __init__(self):
        self.vectorizer = None
        self.requests_vectors = None
        self.responses = None

    def fit(self, requests: str, responses: str):
        pass

    def get_candidate(self, request: str, k=1) -> List[str]:
        pass

    def dump(self, dst_path: str):
        with open(dst_path, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(src_path: str) -> DialoguesBase:
        with open(src_path, 'wb') as f:
            return pickle.load(f)


class PushkinSkill(Skill):
    def __init__(self, data_path):
        self.base = DialoguesBase.load(data_path)

    def match(self, message: str) -> bool:
        return True

    def answer(self, message: str) -> str:
        return random.choice(self.base.get_candidate(message, 5))
