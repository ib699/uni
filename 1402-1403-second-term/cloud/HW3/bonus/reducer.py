#!/usr/bin/env python
from collections import defaultdict
import sys
import heapq

inverted_index = defaultdict(list)

for line in sys.stdin:
    word, count, doc_id = line.strip().split('\t')
    count = int(count)
    inverted_index[doc_id].append((word, count))

K = 3  # Change this value to set the desired number of top words

for doc_id, word_counts in inverted_index.items():
    top_k_words = heapq.nlargest(K, word_counts, key=lambda x: x[1])
    print(f"Document: {doc_id}")
    for word, count in top_k_words:
        print(f"{word}\t{count}")
    print()

