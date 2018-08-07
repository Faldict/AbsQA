import re
import json
import hashlib

DATASET = '../data/dataset.tsv'
data = []
questions = [
    'What model does this paper propose?',
    'What is this model based on?',
    'How does the proposed model differ from previous models?',
    'What algorithm does this paper propose?',
    'What is this algorithm based on?',
    'How does the proposed algorithm differ from previous algorithms?'
]

total = 0
with open(DATASET, 'r') as f:
    line = f.readline()
    while line:
        cols = line.strip().split('\t')
        if len(cols) == 7:
            abstract = cols[-1]
            paragraph = {
                'context': abstract,
                'qas': []
            }

            for i in range(6):
                start_pos = abstract.find(cols[i])
                if start_pos != -1 and len(cols[i]) > 0:
                    paragraph['qas'].append({
                        'id': hashlib.md5(str(cols[i]).encode('utf-8')).hexdigest(),
                        'question': questions[i],
                        'answers': [{
                            'text': cols[i],
                            'answer_start': start_pos,
                        }]
                    })
                    total += 1

            data.append({
                'paragraphs': [paragraph]
            })
        try:
            line = f.readline()
        except:
            continue

dataset = {'data': data}
with open('../data/absqa-train.json', 'w') as f:
    f.write(json.dumps(dataset))

print("Write %s QA pairs!" % total)
