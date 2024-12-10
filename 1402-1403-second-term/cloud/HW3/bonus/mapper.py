#!/usr/bin/env python
import sys
from collections import defaultdict

for line in sys.stdin:
    doc_id, context = line.strip().split(',')
    words = context.split()

    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1

    for word, count in word_count.items():
        print(f"{word}\t{count}\t{doc_id}")

