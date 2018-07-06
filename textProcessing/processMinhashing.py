from datasketch import MinHash
from databaseWorker import get_all_preprocess
from tqdm import tqdm
import os
import pickle

#Text = "hallo ich bin marvin und wohne in berlin Ich bin 23 jahre alt und studiere angewandte informatik"
#Text2 = "hallo ich bin ophelie und wohne in berlin Ich bin 13 jahre alt und studiere informatik"
#preCursor = [Text, Text2]


def udpateMinHash(minHash: MinHash, text: str):
    words = text.split(" ")
    for word in words:
        minHash.update(word.encode('utf8'))

    return minHash


#accuracies = []
#index = []
#first = True
def saveAllMinHashes():
    preCursor = get_all_preprocess()
    allMinHashes = []
    for doc in tqdm(preCursor, "Searching duplicates", preCursor.count()):
        minHash = udpateMinHash(MinHash(512), doc["cleanedText"])
        allMinHashes.append({
            "gruppe": doc["gruppe"],
            "identifier": doc["identifier"],
            "hash": minHash
        })

    with open('minHashesBinary.pickle', 'wb') as handle:
        pickle.dump(allMinHashes, handle)
        handle.close()


def loadAllMinhashes():
    with open('minHashesBinary.pickle', 'rb') as handle:
        unpickler = pickle.Unpickler(handle)
        # if file is not empty scores will be equal
        # to the value unpickled
        hashes = unpickler.load()
    return hashes


def getId(minHasDict):
    return str(minHasDict["identifier"])


def checkAllMinHashesForPossibleDuplications(threshold=0.6):
    allMinHashes = loadAllMinhashes()
    checkedMinHashes = {}
    for textToTest in tqdm(allMinHashes, "Minhashes check", len(allMinHashes)):
        identifier = getId(textToTest)
        foundSimilarArticleIds = []
        for textToCheck in allMinHashes:
            checkedIdentifier = getId(textToCheck)
            if (checkedIdentifier != identifier
                    and textToTest["gruppe"] != textToCheck["gruppe"]):
                accuracy = textToTest["hash"].jaccard(textToCheck["hash"])
                if (accuracy > .5 and accuracy < 1):
                    foundSimilarArticleIds.append((checkedIdentifier,
                                                   accuracy))

        checkedMinHashes[identifier] = foundSimilarArticleIds

    return checkedMinHashes


MODE = "load"

if (MODE == "save"):
    saveAllMinHashes()
elif (MODE == "load"):
    allCheckedArticles = checkAllMinHashesForPossibleDuplications()
    with open('similarBinary.pickle', 'wb') as handle:
        pickle.dump(allCheckedArticles, handle)
        handle.close()
else:
    with open('similarBinary.pickle', 'rb') as handle:
        unpickler = pickle.Unpickler(handle)
        # if file is not empty scores will be equal
        # to the value unpickled
        similarArray = unpickler.load()
