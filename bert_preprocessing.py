import pickle

import numpy as np
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader
from transformers import BertTokenizer, BertModel

from preprocessing import load_lines


def add_negative_samples(requests, responses, k_samples=1):
    n = len(requests)
    requests_data = [requests]
    responses_data = [responses]
    labels = [np.ones(n)]
    for k in range(k_samples):
        requests_data.append(requests)
        responses_data.append(responses[np.random.permutation(n)])
        labels.append(np.zeros(n))
    return np.concatenate(requests_data), np.concatenate(responses_data), \
           np.concatenate(labels)


def subsample(requests, responses, part: float):
    mask = np.random.rand(len(requests)) < part
    return requests[mask], responses[mask]


def build_dataset(requests_path: str, responses_path: str,
                  k_samples=5, part=1.0, test_size=0.3, max_length=64,
                  model_name='DeepPavlov/rubert-base-cased-conversational'):
    requests = np.array(load_lines(requests_path))
    responses = np.array(load_lines(responses_path))
    requests, responses = subsample(requests, responses, part)
    train_requests, test_requests, train_responses, test_responses = \
        train_test_split(requests, responses)
    train_requests, train_responses, train_labels = add_negative_samples(
        train_requests, train_responses, k_samples)
    test_requests, test_responses, test_labels = add_negative_samples(
        test_requests, test_responses, k_samples)
    tokenizer = BertTokenizer.from_pretrained(model_name)
    train_ids = tokenizer(train_requests.tolist(),
                          text_pair=train_responses.tolist(),
                          max_length=max_length, padding='max_length',
                          truncation=True, return_tensors='pt')
    train_labels = torch.tensor(train_labels, dtype=torch.long)
    test_ids = tokenizer(test_requests.tolist(),
                         text_pair=test_responses.tolist(),
                         max_length=max_length, padding='max_length',
                         truncation=True, return_tensors='pt')
    test_labels = torch.tensor(test_labels, dtype=torch.long)
    torch.save((train_ids, train_labels), 'train_ids.torch')
    torch.save((test_ids, test_labels), 'test_ids.torch')
