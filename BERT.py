from transformers import BertModel, BertTokenizer, BertConfig
import numpy as np
from datetime import datetime as dt


# model = BertModel.from_pretrained('DeepPavlov/rubert-base-cased-conversational')
# tokenizer = BertTokenizer.from_pretrained('DeepPavlov/rubert-base-cased-conversational')
#
# data = tokenizer.encode_plus('Февраль! Достать чернил и плакать', return_tensors='pt')
# res = model(**data)
# print(res)

start = dt.now()
print(start)

requests_file = open("static/documents/requests.txt", "r", encoding="utf-8")
responses_file = open("static/documents/responses.txt", "r", encoding="utf-8")

requests = []
responses = []
target = []

for line in requests_file.readlines():
    requests.append(line[:-1])

for line in responses_file.readlines():
    responses.append(line[:-1])

target = [1] * len(responses)

print(dt.now())

c_req = requests
for i in range(5):
    req = np.array(c_req)
    req = np.random.permutation(req)
    requests += list(req)
    responses += responses
    target += [0] * len(c_req)

print(dt.now())

req_output = open("requests_db.txt", "w", encoding='utf-8')
resp_output = open("responses_db.txt", "w", encoding='utf-8')
req_output.writelines('\n'.join(requests))
resp_output.writelines('\n'.join(responses))

end = dt.now()
print(end - start)

