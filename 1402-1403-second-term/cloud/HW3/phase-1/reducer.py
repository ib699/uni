#!/usr/bin/env python
from collections import defaultdict
import sys

inverted_index = defaultdict(list)

for line in sys.stdin:
    word, doc_id = line.strip().split('\t')
    inverted_index[word].append(doc_id)

for word, doc_ids in inverted_index.items():
    print(f"{word}\t{', '.join(doc_ids)}")

