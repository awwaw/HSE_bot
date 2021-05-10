import random
import re

import torch
from torch import nn, softmax
from transformers import BertModel, BertTokenizer, BertForNextSentencePrediction
from bot.bot import Skill
from bot.skills.pushkin import DialoguesBase, PushkinSkill
from random import uniform


class DeepSkill(Skill):
    def __init__(self, dialogues_base: str, model_state: str, device='cpu',
                 model_name='DeepPavlov/rubert-base-cased-conversational'):
        self.base = DialoguesBase.load(dialogues_base)
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertForNextSentencePrediction.from_pretrained(model_name)
        self.model.load_state_dict(torch.load(model_state))
        self.model.to(device)
        self.model.eval()
        self.device = device

    def match(self, message: str) -> bool:
        if message[0] == '@':
            return message.startswith('@deep')
        return len(re.sub(r'[^а-яА-ЯёЁ 0-9]', '', message)) > 0.6 * len(message)

    def answer(self, message: str) -> str:
        if message.startswith('@deep'):
            message = message[5:].strip()
        candidates = self.base.get_candidate(message, 20)
        data = self.tokenizer([message] * 20, text_pair=candidates, return_tensors='pt',
                              max_length=64, padding='max_length', truncation=True)
        with torch.no_grad():
            prediction = self.model(data.input_ids.to(self.device),
                                    attention_mask=data.attention_mask.to(self.device),
                                    token_type_ids=data.token_type_ids.to(self.device))
        probabilities = softmax(prediction.logits, dim=1).detach().cpu().numpy()[:, 1]
        return random.choices(candidates, weights=probabilities, k=1)[0]
