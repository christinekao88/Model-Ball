import csv
import json

csvfile = open('/Users/kao_oak/Desktop/KAO_Ubuntu/ELK/logstash/data/mlb_test2/mlb_test2.csv', 'r',encoding='big5')
jsonfile = open('mlb_test.json', 'w',encoding='big5')

fieldnames = ("num","search","date","username","geo","nretweets","nreplies","nlikes","tweet","place","hashtags","cashtags","retweet","reply_to","link")

reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
print("finished")