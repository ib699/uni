#!/usr/bin/env python
import sys

for line in sys.stdin:
    doc_id, context = line.strip().split(',')
    words = context.split()
    
    for word in words:
        print(f"{word}\t{doc_id}")

