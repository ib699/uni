#!/usr/bin/env bash

# install deps
git clone https://github.com/sadegh-msm/hind.git
cd hind
badh master-build.sh

# edit mapper
echo "#!/usr/bin/env python
import sys

for line in sys.stdin:
    doc_id, context = line.strip().split(',')
    words = context.split()
    
    for word in words:
        print(f\"{word}\t{doc_id}\")
" > mapper.py

echo "#!/usr/bin/env python
from collections import defaultdict
import sys

inverted_index = defaultdict(list)

for line in sys.stdin:
    word, doc_id = line.strip().split('\t')
    inverted_index[word].append(doc_id)

for word, doc_ids in inverted_index.items():
    print(f\"{word}\t{', '.join(doc_ids)}\")
" > reducer.py

# copy mapper, reducer and input.txt
docker cp reducer.py hadoop-namenode:/home
docker cp mapper.py hadoop-namenode:/home
docker cp input.txt hadoop-namenode:/home

# connect to name node container
docker ps -a
docker exec -it hadoop-namenode /bin/bash

# upload input file to hdfs
hdfs dfs -mkdir hdfs://hadoop-namenode:9000/user/
hdfs dfs -mkdir hdfs://hadoop-namenode:9000/user/root
hdfs dfs -put /home/input.txt hdfs://hadoop-namenode:9000/user/root/

# run hadoop
hadoop jar /opt/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -file mapper.py -mapper mapper.py -file reducer.py -reducer reducer.py -input input.txt -output output

# ls the oput directory
hdfs dfs -ls hdfs://hadoop-namenode:9000/user/root/output/

# cat the output
hdfs dfs -cat hdfs://hadoop-namenode:9000/user/root/output/part-00000
