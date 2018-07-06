import numpy as np
import spacy

nlp = spacy.load('de')  # make sure to use larger model!

text = '''Rice Pudding - Poem by Alan Alexander Milne
What is the matter with Mary Jane?
She's crying with all her might and main,
And she won't eat her dinner - rice pudding again -
What is the matter with Mary Jane?
What is the matter with Mary Jane?
I've promised her dolls and a daisy-chain,
And a book about animals - all in vain -
What is the matter with Mary Jane?
What is the matter with Mary Jane?
She's perfectly well, and she hasn't a pain;
But, look at her, now she's beginning again! -
What is the matter with Mary Jane?
What is the matter with Mary Jane?
I've promised her sweets and a ride in the train,
And I've begged her to stop for a bit and explain -
What is the matter with Mary Jane?
What is the matter with Mary Jane?
She's perfectly well and she hasn't a pain,
And it's lovely rice pudding for dinner again!
What is the matter with Mary Jane?'''

doc = nlp(text)


def simFunction(sent1, sent2):
    return nlp(sent1).similarity(nlp(sent2))


def sim2Funtion(sent1, sent2):
    return 1


class TextRank:
    def __init__(self, sentences, simFunction):
        self.sentences = sentences
        self.similarity = simFunction
        self.similarityMatrix = []
        self.calculateGraphWeights(self.sentences)
        self.similarityMatrix = np.array(self.similarityMatrix)
        self.applySoftmax()
        self.ranking = np.full(
            len(sentences), 1 / len(sentences), np.dtype(float))
        self.iterateTextRank()

    def softmax(self, x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def applySoftmax(self):
        for i in range(len(self.similarityMatrix)):
            self.similarityMatrix[:, i] = self.softmax(
                self.similarityMatrix[:, i])

    def calculateGraphWeights(self, sentences):
        for i in range(len(sentences)):
            self.similarityMatrix.append([])
            for j in range(len(sentences)):
                if (i != j):
                    self.similarityMatrix[-1].append(
                        self.similarity(
                            sentences[i], sentences[j]
                        )
                    )
                else:
                    self.similarityMatrix[-1].append(0)

    def iterateTextRank(self):
        for i in range(len(self.sentences)):
            self.ranking = np.dot(self.similarityMatrix, self.ranking.T)





sentences = [sent.text for sent in doc.sents]
k = TextRank(sentences, simFunction)

maxIndex = np.argmax(k.ranking)
print(sentences[maxIndex])
