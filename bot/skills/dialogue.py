import torch
from torch import nn, sigmoid
from transformers import BertModel, BertTokenizer
from bot.bot import Skill
from bot.skills.pushkin import DialoguesBase, PushkinSkill
from random import uniform


class DialogueSkill(Skill):
    def __init__(self, sequence: str = None):
        self.bert_model = BertModel.from_pretrained('DeepPavlov/rubert-base-cased-conversational')
        self.bert_tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased-conversational')

        self.model = nn.Sequential(
            nn.Linear(768, 256),
            nn.ReLU(),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
        self.base = DialoguesBase.load('static/documents/save_state.tmp')

        self.model.load_state_dict(torch.load('static/model/model.torch'))

    def match(self, sequence: str) -> bool:
        return True

    def answer(self, sequence: str) -> str:
        candidates = self.base.get_candidate(sequence, 20)
        data = self.bert_tokenizer([sequence] * 20, text_pair=candidates, return_tensors='pt',
                                   max_length=64, padding='max_length', truncation=True)
        res = self.bert_model(**data)
        predictions = sigmoid(self.model(res.pooler_output)).detach().numpy()
        mx = [-1, -1]
        for i in range(len(predictions)):
            if predictions[i] > mx[0]:
                mx[0] = predictions[i]
                mx[1] = i

        arr = []
        for ind, val in enumerate(predictions):
            arr.append((val, ind))
        arr.sort(reverse=True)
        arr = arr[:5]
        pref = (list(map(lambda x: abs(x[0][0]), arr)))
        num = uniform(0, sum(pref))
        pref_s = [0]
        for i in range(len(pref)):
            pref_s.append(pref_s[i] + abs(pref[i]))

        ind = -1
        for i in range(len(pref_s) - 1):
            if pref_s[i] <= num <= pref_s[i + 1]:
                ind = i
                break

        return candidates[ind]


