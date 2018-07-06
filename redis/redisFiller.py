import redis
from tqdm import tqdm

stopWordFile = open("morphy-mapping-20110717.csv")
stopwords = stopWordFile.read().splitlines()
stopWordFile.close()
stopwords = list(map(lambda stopword: { "key": stopword.split(',')[0], "value": stopword.split(',')[1]}, stopwords))
r = redis.StrictRedis(host='localhost', port=6379, db=1)

for dict in tqdm(stopwords):
    r.set(dict.get("key"), dict.get("value"))
    r.set(dict.get("value"), dict.get("value"))
    #print(dict.get("key"), " - ", dict.get("value"))
