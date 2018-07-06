import unittest
from TextProcessing import removeSpecialChars, removeStopWords


class TestTextProcessing(unittest.TestCase):
    def test_remove_chars_beginning(self):
        self.assertEqual(removeSpecialChars('    0 0 0 asnaasfa'), 'asnaasfa')

    def test_end_text_remove(self):
        self.assertEqual(
            removeSpecialChars(
                "Außerdem müsste vertraglich eine Fertigstellungsgarantie von Hertha zugesichert werden.      Mehr zum Thema: Pläne veröffentlicht: So soll Herthas neues Stadion aussehen     ( dpa/BM )    © Berliner Morgenpost 2018 – Alle Rechte vorbehalten."
            ),
            "Außerdem müsste vertraglich eine Fertigstellungsgarantie von Hertha zugesichert werden"
        )

    def test_full_example_one(self):
        self.assertEqual(
            removeSpecialChars(
                " 00 - 00 Dr. Prof. nat. er. Kühn-Loggo: 'Sei ruhig', sagt er vorlaut!"
            ), "Dr Prof nat er KühnLoggo Sei ruhig sagt er vorlaut")

    def test_full_example_two(self):
        self.assertEqual(
            removeSpecialChars(
                "      0    0                Berlin. Hertha BSC ist mit seinen Plänen für ein neues Stadion auf Skepsis im Berliner Abgeordnetnehaus gestoßen. Vertreter aller Fraktionen machten am Freitag im Sportauschuss deutlich, dass aus ihrer Sicht noch viele Fragen offen sind und ein längerer Diskussionsprozess bevorsteht. Einige Parlamentarier kritisierten auch die öffentlich dokumentierte Vorfestlegung der Hertha für einen Stadionneubau. Der Senat verhandelt seit Juli 2017 mit dem Bundesligisten. In der Vorwoche hatten beide Seiten mitgeteilt, dass sie zwei Varianten für \"technisch realisierbar\" halten: den Umbau des Olympiastadions oder einen Neubau im Olympiapark nebenan. Hertha bevorzugt einen Neubau, den der Verein selbst finanzieren will. Der Senat favorisiert dagegen aus Angst vor finanziellen Einbußen den Hertha-Verbleib in seiner alten Arena. Es ist das Anliegen des Senats, Hertha in Berlin zu halten. Der monetäre Nutzen für die Stadt Berlin vom Wirtschaftsunternehmen Hertha BSC liegt im dreistelligen Millionenbereich. Der aktuelle Mietvertrag für das Olympiastadion läuft 2025 aus.     Die Debatte im Sportausschuss im Minutenprotokoll Innensenator Geisel, der auch für Sport zuständig ist, führt aus, dass es für den Senat höchste Priorität hat, dass das Olympiastadion wirtschaftlich zu betreiben ist. Geisel: \"Die Vorzugsvariante des Landes Berlin ist, dass Hertha weiter im Olympiastadion spielt. Wenn möglich mit einer Modernisierung, aber ohne großen Umbau. Wir nehmen zur Kenntnis, dass Hertha andere Vorstellungen hat. Die halte ich nicht für illegitim. Weil die Mehrzahl der Bundesliga-Konkurrenten in Fußballstadion spielt. Insofern müssen wir erkennen, dass die Modernisierung sich allein nicht stellt.\"           Die Kosten für den Umbau werden auf 160, 165 Millionen geschätzt, dazu die LED-Vorhänge auf rund 30 Millionen. Insgesamt würde die Variante 190 Millionen kosten. Das Geld wäre aus dem Landeshaushalt des Landes Berlin zu bezahlen. Im Falle eines Neubaus betont Geisel die Wichtigkeit einer Konkurrenzausschlussklausel. Konzerte und, hier wiederholt er seine Interpretation \"die großen Spiele von Hertha\" müssten im Olympiastadion stattfinden. Außerdem müsste vertraglich eine Fertigstellungsgarantie von Hertha zugesichert werden.      Mehr zum Thema: Pläne veröffentlicht: So soll Herthas neues Stadion aussehen     ( dpa/BM )    © Berliner Morgenpost 2018 – Alle Rechte vorbehalten."
            ),
            "BerlinHertha BSC ist mit seinen Plänen für ein neues Stadion auf Skepsis im Berliner Abgeordnetnehaus gestoßen Vertreter aller Fraktionen machten am Freitag im Sportauschuss deutlich dass aus ihrer Sicht noch viele Fragen offen sind und ein längerer Diskussionsprozess bevorsteht Einige Parlamentarier kritisierten auch die öffentlich dokumentierte Vorfestlegung der Hertha für einen Stadionneubau Der Senat verhandelt seit Juli 2017 mit dem Bundesligisten In der Vorwoche hatten beide Seiten mitgeteilt dass sie zwei Varianten für technisch realisierbar halten den Umbau des Olympiastadions oder einen Neubau im Olympiapark nebenan Hertha bevorzugt einen Neubau den der Verein selbst finanzieren will Der Senat favorisiert dagegen aus Angst vor finanziellen Einbußen den HerthaVerbleib in seiner alten Arena Es ist das Anliegen des Senats Hertha in Berlin zu halten Der monetäre Nutzen für die Stadt Berlin vom Wirtschaftsunternehmen Hertha BSC liegt im dreistelligen Millionenbereich Der aktuelle Mietvertrag für das Olympiastadion läuft 2025 aus     Die Debatte im Sportausschuss im Minutenprotokoll Innensenator Geisel der auch für Sport zuständig ist führt aus dass es für den Senat höchste Priorität hat dass das Olympiastadion wirtschaftlich zu betreiben ist Geisel Die Vorzugsvariante des Landes Berlin ist dass Hertha weiter im Olympiastadion spielt Wenn möglich mit einer Modernisierung aber ohne großen Umbau Wir nehmen zur Kenntnis dass Hertha andere Vorstellungen hat Die halte ich nicht für illegitim Weil die Mehrzahl der BundesligaKonkurrenten in Fußballstadion spielt Insofern müssen wir erkennen dass die Modernisierung sich allein nicht stellt           Die Kosten für den Umbau werden auf 160 165 Millionen geschätzt dazu die LEDVorhänge auf rund 30 Millionen Insgesamt würde die Variante 190 Millionen kosten Das Geld wäre aus dem Landeshaushalt des Landes Berlin zu bezahlen Im Falle eines Neubaus betont Geisel die Wichtigkeit einer Konkurrenzausschlussklausel Konzerte und hier wiederholt er seine Interpretation die großen Spiele von Hertha müssten im Olympiastadion stattfinden Außerdem müsste vertraglich eine Fertigstellungsgarantie von Hertha zugesichert werden"
        )

    def test_remove_stop_words(self):
        self.assertEqual(
            removeStopWords(
                "Ab nach Hause zu meiner Mama, denn keineswegs kann das hier wahr sein."
            ), "Ab Hause Mama, wahr sein.")


if __name__ == '__main__':
    unittest.main()