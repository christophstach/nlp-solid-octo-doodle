import redis
import databaseWorker
import TextProcessing
import logging
from threading import Thread
from tqdm import tqdm

# for checking if article is already pre-processed.


def worker_for_group(i):
    def worker():
        collection = databaseWorker.get_articles_from_group(i)
        for doc in tqdm(collection.find(),
                        "Preprocessing Tables from Group " + str(i),
                        collection.find().count()):
            identifier = doc["_id"]
            gruppe = i
            exsistsAlready = databaseWorker.hasPreprocessedArticle(
                gruppe, identifier)
            if (exsistsAlready == False):
                cleanedText = TextProcessing.preprocessing(doc["text"])
                cleanedArticle = databaseWorker.PreprocessedArticle(
                    gruppe, identifier, cleanedText)
                successfully = databaseWorker.savePreprocessedArticle(
                    cleanedArticle)
                if (successfully == False):
                    print("!!!!!!!!!!!! EERRRRRRORRRRRRR !!!!!!!!!!!!!!!!")

    return worker


threads = []
for i in range(1, 5):
    logging.log(logging.DEBUG, "Thread {", i, "} started")
    t = Thread(target=worker_for_group(i))
    threads.append(t)
    t.start()

for thread in threads:
    thread.join()