import collections
import json

with open("corpus.txt", 'r') as f:
	model = collections.defaultdict(lambda: 1)
	features = [x.strip() for x in f.read().split('\n') if len(x.strip())>0]
	print("Lista la lista cole!!")
	i = 0
	for feature in features:
		model[feature] += 1
		i += 1
		if i in [1000, 3000, 5000, 10000, 50000]:
			print("Van "+str(i))  

with open('corpus.json', 'w', encoding='utf8') as json_file:
	json.dump(model, json_file, ensure_ascii=False)

