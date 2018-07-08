from pprint import pprint

from nlp_utils import build_weights_matrix, \
    extract_sentences, extract_unique_words, extract_noun_chunks, \
    spacy_similarity
from weighted_page_rank import WeightedPageRank

text = '''An der Rudolf-Wissell-Brücke in Charlottenburg wird mal wieder gebaut. Damit die marode Piste auf einer der 
meistbefahrenen Autobahnabschnitte der Republik überhaupt noch befahren werden kann, werden rund sieben Millionen 
Euro investiert. In sieben Wochen sollen die Arbeiten abgeschlossen sein – bevor dann im Jahr 2023 die Arbeiten für 
einen Neubau beginnen. Auch wenn Berlins Autofahrer darüber stöhnen, dass sie sich nun wieder wochenlang im Stau 
stehen – eine Alternative zu diesen Arbeiten gibt es nicht. Dass dafür die Sommerferien genutzt werden, in der bis zu 
30 Prozent weniger Kraftfahrzeuge die Stadtautobahn passieren, ist zudem vernünftig. Noch besser wäre es, 
wenn die Berliner Verkehrsverwaltung gerade im Hinblick auf das zu erwartenden Verkehrschaos im Zuge des Neubaus ein 
Projekt wieder aufleben lassen würde, das den Hauptstädtern schon vor vielen Jahren in Aussicht gestellt wurde: Eine 
Zusatz-Maut für Lastwagen auf der Stadtautobahn. Tatsächlich nutzen unzählige Lkw-Fahrer im Transitverkehr die A 100 
als Abkürzung auf der Nord-Süd-Route. 25 Kilometer kürzer ist die Strecke quer durch Stadt. Je nach Schadstoffklasse 
oder Achszahl ist die fahrt quer durch die Stadt eine Handvoll Euros günstiger als die Umfahrung über den Berliner 
Ring. Ein falscher Anreiz, der dringend behoben werden muss, bevor in einigen Jahren die Wissell-Brücke zur 
Dauerbaustelle wird. Solch eine Maut wollte schon die damalige Verkehrssenatorin Ingeborg Junge-Reyer (SPD) einführen 
lassen. Aber wie so oft in Berlin blieb es bei der Ankündigung, Taten folgten den Worten nicht. Selbst die 
Prüforganisation Dekra, zu deren Mitgliedern überwiegend Firmen mit gewerblichen Fuhrparks gehören, räumt ein, 
dass eine solche Maut sinnvoll ist. Noch wäre Zeit eine entsprechende Bundesratsinitiative zu starten, damit ab 2023 
kein Lkw-Fahrer dafür belohnt wird, wenn er die Stadtautobahn verstopft.'''

print('''
####################################
# Summary                          #
####################################
''')
sentences = extract_sentences(text)
weights = build_weights_matrix(tokens=sentences, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights, iterations=len(sentences))
print(' '.join(pr.get_top_entries(sentences, count=2)))

print('''
####################################
# Keywords (noun chunks)           #
####################################
''')
noun_chunks = extract_noun_chunks(text)
weights = build_weights_matrix(tokens=noun_chunks, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights, iterations=len(noun_chunks))
print(', '.join(pr.get_top_entries(noun_chunks, count=5, keep_original_occurrence=False)))

print('''
####################################
# Keywords (words)                 #
####################################
''')
words = extract_unique_words(text)
weights = build_weights_matrix(tokens=words, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights, iterations=len(words))
print(', '.join(pr.get_top_entries(words, count=8, keep_original_occurrence=False)))
