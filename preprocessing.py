import re
import sys
from typing import List
from nltk.stem.snowball import RussianStemmer


def tokenize(src_path: str, dst_path: str):
    lines = load_lines(src_path)

    result = []
    non_letters = re.compile(r'[^a-zA-Zа-яА-Яе-ё ]')
    for line in lines:
        line = non_letters.sub(' ', line)
        tokens = line.strip().lower().split()
        result.append(' '.join(tokens))

    store_lines(dst_path, result)


def apply_lemmatization(src_path: str, dst_path: str):
    lines = load_lines(src_path)

    result = []

    # TODO apply lemmatization

    store_lines(dst_path, result)


def apply_stemming(src_path: str, dst_path: str):
    lines = load_lines(src_path)
    stemmer = RussianStemmer()
    result = []
    for sentence in lines:
        stemmed = []
        p = re.compile(r'[^a-zA-Zа-яА-Яе-ё ]')
        words = p.sub(' ', sentence).split()
        for word in words:
            stemmed.append(stemmer.stem(word))
        result.append(" ".join(stemmed))
    store_lines(dst_path, result)


def load_lines(src_path: str) -> List[str]:
    with open(src_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


def store_lines(dst_path: str, lines: List[str]):
    with open(dst_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))


def main(algorithm, src_path, dst_path):
    if algorithm == 'tokenization':
        tokenize(src_path, dst_path)
    elif algorithm == 'stemming':
        apply_stemming(src_path, dst_path)
    elif algorithm == 'lemmatization':
        apply_lemmatization(src_path, dst_path)
    else:
        print('Unknown algorithm requested!')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
