docker cp input2.txt hadoop-namenode:/home

docker exec -it hadoop-namenode /bin/bash
cd home/


hdfs dfs -put /home/input2.txt hdfs://hadoop-namenode:9000/user/root/

hadoop jar /opt/hadoop-3.3.6/share/hadoop/tools/lib/hadoop-streaming-3.3.6.jar -file mapper.py -mapper mapper.py -file reducer.py -reducer reducer.py -input input2.txt -output output
