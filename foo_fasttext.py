import fasttext

classifier = fasttext.supervised('train_plag_data.txt', 'model')

result = classifier.test('test_plag_data.txt')

print('Precision:', result.precision)
print('Recall:', result.recall)
print('Number of examples:', result.nexamples)
