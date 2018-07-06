## Vergleich von Dokumente mit Word2Vec und Nominal-Phrasen

Zur Aufgabe habe ich es mir gemacht Dokumente auf semantischen Inhalt zu vergleichen. Dazu sollte die Library Word2Vec von Gensim benutzen, welche Word-Embeddings generiert.
Word Embeddings sind Wörter die zu Vektoren umgewandelt wurden. Das Word2Vec Model soll mit den jeweiligen Nominal-Phrasen aus den Artikeln trainiert werden.
Nominal-Phrasen sind sind mehrere Wörter die zusammengehören und als Kern ein Substantiv haben.

Angefangen wurde mit dem Preprocessing. Hierzu wird die Library spaCy benutzt die viele Funktionen bietet und meiner Meinung nach ein Preprocessing sehr einfach macht.
Um ein Word2Vec Model für Genesim trainieren zu können, erwartet Gensim Daten in folgender Form:

```python
[
    ['mein', 'erster', 'Satz', 'ist', 'dieser', '.'],
    ['und', 'das', 'ist', 'mein', 'zweiter', '.']
]
```

### Preprocessing *(Update)*
    
Gensim erwartet ein Array von Arrays (Sätzen), die jeweils die einzelnen Wörter als Array Elemente beinhalten.
Da wir komplette Dokumente (News-Artikel-Texte) in der Datenbank gespeichert haben, sieht das Preprocessing folgendermaßen aus:

- Fehlerhafte Unicode-Codierungen und unbekannte Zeichen entfernen
- Sätze wie "Berliner Morgenpost 2018 Alle Rechte vorbehalten" entfernen
- "&" mit "und" ersetzen"
- Doppelte Leerzeichen entfernen
- Text in Sätze aufteilen und diese als Array speichern
    - Hierzu kann man sehr komfortabel mit spaCy arbeiten siehe:
     
    ```python
    nlp = spacy.load('de')
    doc = nlp(text)
    sentences = []
        for sentence in doc.sents:  # Split text into sentences
            sentences.append(sentence)
    # ...
    ```
- Die einzelnen, enstandenen Sätze in Nominal-Phrasen aufteilen
    - Auch hier kann spaCy sehr gut verwendet werden:
    
    ```python
    for chunk in sentence.noun_chunks:  # Get noun_chunks out of sentence
    # ...
    ```
- Die einzelnen Texte in Kleinschreibung formatieren
- Die einzelnen Texte lemmatisieren (hierzu wurde die von Marvin und Ophélie Lemmantiesierungs-Methode benutzt)

Einige Bespiele und deren Ergebnis nach dem Preprocessing:


```python
# EU-Justizkommissarin Vera Jourova hat vor einer zunehmenden Beeinflussung von Wählern im Internet gewarnt.
[
    'eu-justizkommissari vera jourova',
    'zunehmend beeinflussung',
    'wahl',
    'inter'
]

# Der Datenskandal um Facebook und Cambridge Analytica, von dem auch 2,7 Millionen EU-Bürger betroffen waren, sei ein Weckruf für den Datenschutz, sagte Jourova.
[
    'datenskandal',
    'facebook',
    'cambridg analytica',
    '2,7 millio eu-burg',
    'weckruf',
    'datenschutz',
    'jourova'
]

# Aber fünf Jahre nach dem Start des Prozesses sind bisher erst zwei Bauprojekte mit zusammen knapp 150 Wohnungen fertiggestellt, weitere knapp 700 sind im Bau.
[
    'start',
    'prozess',
    'bauprojek',
    'knapp 150 wohnung',
    'bauen'
]

# Noch 2018 würden auf den ehemaligen Landesgrundstücken 400 Wohnungen fertig, 2019 seien 1400 avisiert und für 2020 dann 2400.
[
    'ehemalig landesgrundstuck',
    '400 wohnung'
]
```


### Word2Vec

Mit den vorverarbeitet Daten kann das Word2Vec Model trainiert werden, um Word Embeddings zu erstellen.
Um das Word2Vec Model zu erstellen benutze ich die Gensim Library. Bei der Erstellung des Word2Vec Models werden die wie oben gezeigten Arrays als Parameter erwartet.
Außerdem können folgende Parameter bei der Erstellung intressant sein.

 - size: Die Dimensionsgröße der erstellten Word Embeddings:
 - window: Definiert wie weit ein Wort weg sein darf um noch im *Context* zu liegen.
 - min_count: Alle Wörter die nicht mindestens *min_count* mal im Corpus auftreten werden ignoriert.
 
Für das Training meines Models habe ich die Parameter folgendermaßen gewählt: size=300, window=4, min_count=2

Mit folgendem Code kann ein Word2Vec Model erstellt und trainiert werden:

```python
word2vec = Word2Vec(sentences=preprocessed_data, window=4, min_count=2, size=300)
```

Außerdem muss ein Dictionary, BoW-Corpus und ein TfIdf Model erstellt werden, die im späteren Verlauf verwendet werden.

```python
dictionary = Dictionary(preprocessed_data)
bow_corpus = list(map(dictionary.doc2bow, preprocessed_data)) # Bag-Of-Words
tfidf = TfidfModel(bow_corpus)
```

Das Preprocessing sowie die Erstellung des Word2Vec Models dauerte bei 16.000 ca. 20 bis 25 Minunten.

#### Dictionary

In einem Dictionary wird jedem Wort im Corpus eine Id zugewiesen.

#### BoW-Corpus

BoW steht für Bag of Words. Es ist eins der einfachsten Modelle, kann jedoch im späteren Verlauf noch verwendet werden.
Ein BoW speichert jedes Wort mit der Anzahl seiner Vorkommen mit Bezug auf das Dictionary.

Beispiel (nicht aus dem originalen Corpus): 

```python
# ['john', 'likes', 'to', 'watch', 'movies', 'mary', 'likes', 'movies', 'too']
bow = {
    'hello': 0, # Diese Wörter sind nur im Dictionary enthalten aber nicht im Satz
    'not': 0,
    'in': 0,
    'sentences': 0,
    
    'john': 1,
    'likes': 2,
    'to': 1, 
    'watch': 1, 
    'movies': 2,
    'mary': 1, 
    'too': 1
}
```

Für den BoW-Corpus werden für jeden Satz in unserem Corpus ein BoW Model erstellt und diese in einem Array seperat abgespeichert.

#### TfIdf

**TfIdf** steht für **term frequency–inverse document frequency** und ist ein Model was im Gegensatz zu **Bag-Of-Words** eine Gewichtung der einzelnen Wörter mit einbezieht.
Der Tf Teil arbeitet ähnlich wie Bag of Words und gibt Wörtern die öfter in einem Dokument vorkommen ein höheres Gewicht.
Der Idf Teil zählt Wörter über den ganzen Corpus und gibt Wörtern die oft vorkommen ein niedriges Gewicht und Wörtern die selten vorkommen ein hohes.
Somit bekommen seltene Wörter eine hohe Importanz für das Dokument.


## Dokumentenvergleich *(Update)*

Mit den zuvor erstellten Modellen war es möglich einen Vergleich von zwei kompletten Dokmenten vorzunehmen.
Hierzu diente die von Gensim bereitgestellte Funktion `softcossim()`, sie vergleicht zwei Texte im Bag-of-Words Format auf Basis einer Similarity-Matrix-Matrix.

### Similarity Matrix

Einen Similarity Matrix speichert den Vergleich aller Wörter. Dazu werden alle Word-Embeddings (die vorher mit Word2Vec generiert wurden, und die im jeweiligen Dictionary vorkommen) mit sich selbst vergliechen.
Zusätzlich ist es optional möglich die vom TfIdf generierten Gewichtungen mit einzubeziehen.

```python
similarity_matrix = word2vec.wv.similarity_matrix(dictionary, tfidf)
```

### Der Vergleich

Um einen Vergleich zwischen zwei Dokumente zu machen, müssen die Texte jetzt im Preproccesten Format in ein Bag-of-Words Format umgewandelt werden.
Diese Bag-of-Words Formate können über `softcossim()` und der zuvor erstellte `similarity_matrix` verglichen werden.

```python
text1 = '...'
text2 = '...'

preprocessed_text1 = preprocessor.preprocess_text(text1)
preprocessed_text2 = preprocessor.preprocess_text(text2)

bow1 = dictionary.doc2bow(preprocessed_text1)
bow2 = dictionary.doc2bow(preprocessed_text2)

softcossim_similarity = softcossim(bow1, bow2, similarity_matrix)
```

### Evaluation der Accuracy

Um eine Accuracy zu berechnen muss zuerst ein Grenzen (threshold) berechnet werden wie ab welcher Similarity zwei Texte als Dublette gelten sollen.

```python
def is_duplicate(text1, text2, threshold):
    preprocessed_text1 = preprocessor.preprocess_text(data['text1'])
    preprocessed_text2 = preprocessor.preprocess_text(data['text2'])

    bow1 = dictionary.doc2bow(preprocessed_text1)
    bow2 = dictionary.doc2bow(preprocessed_text2)

    softcossim_similarity = softcossim(bow1, bow2, similarity_matrix)

    return softcossim_similarity >= threshold
```

Hierzu wurde der von Laura erstelle Testdatensatz verwendet. Dieser stellt 810 Datensätze zum Training und 69 zum Test bereit.
Ein Datensatz besteht jeweils aus zwei Texten und einer Markierung, die angibt ob es sich bei den zwei Texten um Duplikate handelt.
Nach einer Berechnung der Similarity über alle Train-Datensätze ergibt sich ein **Mean** von `0.8700545432277638`.

Dieser Wert dient als Grenze (threshold) für die Berechnung der Accuracy.
Es wurden für alle Test-Datensätze berechnet ob es sich unter einbeziehung des Thresholds um Duplikate handelt.
Danach wurde lediglich die Anzahl aller korrekt klassifizierten Dubletten durch die Anzahl aller Test-Datensätze geteilt.
Dadurch ergibt sich eine Accuracy von `78.26086956521739 %`

Der dazu verwendete Code:

```python
duplicates = []
none_duplicates = []

train = get_train()

for data in tqdm(train, desc='Calculating similarities'):
    preprocessed_text1 = preprocessor.preprocess_text(data['text1'])
    preprocessed_text2 = preprocessor.preprocess_text(data['text2'])

    bow1 = dictionary.doc2bow(preprocessed_text1)
    bow2 = dictionary.doc2bow(preprocessed_text2)

    softcossim_similarity = softcossim(bow1, bow2, similarity_matrix)

    if data['duplicate']:
        duplicates.append(softcossim_similarity)
    else:
        none_duplicates.append(softcossim_similarity)

sleep(2)
print('Mean duplicates:', mean(duplicates))

print()

mean_duplicates = mean(duplicates)

test = get_test()
correct = 0
total = len(test)

for data in tqdm(test, desc='Calculating duplicates'):
    if data['duplicate'] == is_duplicate(data['text1'], data['text2'], mean_duplicates):
        correct += 1

sleep(2)
print('Correct: ', correct)
print('Total: ', total)
print('Accuracy: ', (correct / total * 100), '%')
```

## Mögliche nächste Schritte und Resümee der bisherigen Arbeit

Zufriedenstellend konnte ein Dokumenten vergleich realisiert werden. 
Die Accuracy könnte durch Verwendung einer anderen Preprocessing-Technik oder die Verwendung eines anderen Word-Embeddings-Models
noch verglichen und verbessert werden. Außerdem werden zur Zeit alle Texte der Datenbank als Corpus verwendet. 
Darunter sind auch doppelte (geänderte Zeitungsartikel). Durch eine Methode wie z.B. **Min-Hashing** könnten diese im Vorfeld bereits gefiltert werden. 
Außerdem sollte das der Vergleich mit steigender Anzahl verschiedener Texte genauer werden.
 
