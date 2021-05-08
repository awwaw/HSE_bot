from sklearn.feature_extraction.text import TfidfVectorizer
import time

from bot.bot import Skill


class TF_IDF(Skill):
    start = time.time()
    stemmed = open("../../stemmed.txt", encoding="utf-8").read().split()
    f = open("../../matrix.txt", "wb")
    vectorizer = TfidfVectorizer(decode_error="ignore", max_features=20)
    vectorizer.fit_transform(stemmed)
    f.close()
    end = time.time()
    print(end - start)