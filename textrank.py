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

text = '''
Nach anhaltender Kritik an seinem Gipfel mit dem russischen Präsidenten Wladimir Putin in Helsinki hat US-Präsident Donald Trump den Kremlchef überraschend im Herbst nach Washington eingeladen.
Die Sprecherin des Weißen Hauses, Sarah Sanders, teilte am Donnerstag (Ortszeit) auf Twitter mit, Trump habe seinen Nationalen Sicherheitsberater John Bolton mit der Einladung betraut. Die US-Opposition forderte Trump dazu auf, zunächst aufzuklären, was er im Vieraugengespräch mit Putin in Helsinki besprochen hat.
Vorher dürfe Trump Putin nicht erneut hinter verschlossenen Türen treffen, verlangte der Oppositionsführer im US-Senat, der Demokrat Chuck Schumer - und zwar weder "in den Vereinigten Staaten, in Russland oder sonstwo". Die Oppositionsführerin im Repräsentantenhaus, Nancy Pelosi, spielte erneut darauf an, dass Putin belastendes Material gegen Trump in der Hand haben könne. "Womit erpresst Putin Präsident Trump, persönlich, politisch oder finanziell?", fragte sie.
US-Geheimdienstkoordinator Dan Coats zeigte sich von der Ankündigung des Weißen Hauses überrascht. Beim Aspen-Sicherheitsforum in Colorado sagte er: "Ich wusste davon nichts." Coats erneuerte seine Vorwürfe gegen die Russen, denen er vorwirft, sich in inneramerikanische Angelegenheiten einzumischen. "Sie sind es, die versuchen, unsere Grundwerte zu untergraben, uns von unseren Alliierten zu entzweien, bei unserem Wahlprozess Chaos anzurichten."
Trump hatte am Donnerstag auf Twitter Kritik an dem "sehr erfolgreichen" Gipfel mit Putin in Helsinki zurückgewiesen und geschrieben: "Ich freue mich auf unser zweites Treffen, damit wir damit beginnen können, einige der vielen diskutierten Themen umzusetzen." Sollte Putin tatsächlich nach Washington kommen, wäre es sein erster Besuch im Weißen Haus seit September 2005, als George W. Bush noch US-Präsident war.
Trump hatte in den Tagen nach dem Gipfel mit Putin am Montag in Helsinki mit widersprüchlichen Aussagen, Dementis und Klarstellungen viel Verwirrung gestiftet. Im Zuge seines Zickzack-Kurses hatte Trump dem US-Sender CBS am Mittwoch gesagt, er habe persönlich Putin davor gewarnt, dass die USA Einmischungen in künftige US-Wahlen nicht tolerieren würden.
Zuvor hatte Trump sich sowohl bei der Pressekonferenz mit Putin in Helsinki als auch am Rande einer Kabinettssitzung am Mittwoch in Washington anders geäußert, dies später aber entweder als Versprecher oder falsche Berichterstattung bezeichnet. Trumps erste Äußerungen legten nahe, dass er Erkenntnisse der US-Geheimdienste anzweifelt. Diese halten es für erwiesen, dass Russland sich in die Präsidentenwahl von 2016 eingemischt hat. Putin bestritt dies am Montag in Helsinki. Trump nannte Putins Dementi "extrem stark und kraftvoll".
Nach einem Bericht der "New York Times" sind Trump bereits zwei Wochen vor dessen Amtseinführung im Januar 2017 streng vertrauliche Geheimdienstinformationen gezeigt worden, wonach Putin persönlich Cyber-Angriffe auf die US-Wahlen angeordnet haben soll. Diese Informationen sollen unter anderem von einer Quelle aus dem engsten Umfeld Putins stammen. Trump habe sich widerwillig überzeugt gezeigt, berichtete das Blatt.
Obwohl Trump in den vergangenen Tagen mit seinen widersprüchlichen Aussagen selbst die Kontroverse befeuert hatte, machte er am Donnerstag die Berichterstattung in einigen Medien dafür verantwortlich. Er warf ihnen dabei unter anderem Kriegstreiberei vor: "Die Fake-News-Medien wollen unbedingt eine große Konfrontation sehen, sogar eine Konfrontation, die zum Krieg führen könnte", schrieb er auf Twitter. Trump schien auch auf den Bericht in der "New York Times" angespielt zu haben.
Die sogenannten Fake-News-Medien erfänden Geschichten, ohne dafür Quellen oder Beweise zu haben, twitterte Trump. "Viele Beiträge, die über mich oder die guten Leute um mich herum geschrieben werden, sind reine Fiktion." Mit Fake-News-Medien meint Trump pauschal alle, die nicht auf einer Welle mit ihm liegen oder kritisch über ihn berichten. Dazu gehören auch Zeitungen wie die angesehene "New York Times", die Jahr für Jahr mit Journalistenpreisen für ihre Qualitätsberichterstattung geehrt wird.
'''

print('''
####################################
# Summary                          #
####################################
''')
sentences = extract_sentences(text)
weights = build_weights_matrix(
    tokens=sentences, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights)
print(' '.join(pr.get_top_entries(sentences, count=2)))

print('''
####################################
# Keywords (noun chunks)           #
####################################
''')
noun_chunks = extract_noun_chunks(text)
weights = build_weights_matrix(
    tokens=noun_chunks, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights)
print(', '.join(pr.get_top_entries(noun_chunks,
                                   count=5, keep_original_occurrence=False)))

print('''
####################################
# Keywords (words)                 #
####################################
''')
words = extract_unique_words(text)
weights = build_weights_matrix(
    tokens=words, comparator=spacy_similarity, normalize=True)
pr = WeightedPageRank(weights=weights)
print(', '.join(pr.get_top_entries(words, count=8, keep_original_occurrence=False)))
