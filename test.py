from ElizaSkill import ElizaSkill

x = ElizaSkill(None)
x.post = {
    "I'm": ["You", "are"],
    "my": ["your"]
}

print(x.postprocess(["It's", "my", "apple"]))