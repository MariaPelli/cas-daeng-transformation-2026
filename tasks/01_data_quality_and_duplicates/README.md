# Aufgabe 1: Datenqualität, Duplikate und Dubletten

[Zur Workshop-Übersicht](../../workshop/README.md)

Ihr untersucht den Rohdatensatz, formuliert Hypothesen und klärt, weshalb mehrere ähnliche Zeilen nicht automatisch dasselbe bedeuten.

## Ausgangslage

MetroPulse Operations beobachtet in einem operativen Dashboard ungewöhnlich hohe Fahrtenzahlen. Gleichzeitig stimmen einzelne Umsatzsummen nicht mit einer Kontrollrechnung überein. Das Plattformteam vermutet, dass ein Teil der Daten erneut eingelesen wurde. Die Finanzabteilung weist jedoch darauf hin, dass negative Beträge auch legitime Gegenbuchungen darstellen können.

Ihr sollt herausfinden, welche Erklärungen durch die Daten gestützt werden. Noch soll nichts endgültig gelöscht werden.

## Dateien

Ausgangsdaten:

```text
data/input/trips\_case\_initial.parquet
```

Arbeitsnotebook:

```text
tasks/01\_data\_quality\_and\_duplicates/task.ipynb
```

Falls das Notebook noch nicht bereitgestellt ist, könnt ihr die beschriebenen Schritte in einem neuen Notebook im Aufgabenordner durchführen.

## Lernziele

Nach der Aufgabe könnt ihr:

* Datenqualität anhand konkreter Analyseziele beurteilen;
* Missingness als mögliches Muster statt nur als Fehler untersuchen;
* exakte Duplikate mit einer fachlich sinnvollen Spaltenauswahl bestimmen;
* Near-Duplicates über mehrere Attribute und Toleranzen finden;
* technische Replay-Ereignisse von finanziellen Gegenbuchungen unterscheiden;
* Entscheidungen, Unsicherheiten und Auswirkungen dokumentieren.

## Teil A: EDA und Hypothesen

Erstellt zunächst ein kompaktes Profil des Datensatzes. Untersucht mindestens:

* Anzahl Zeilen und Spalten;
* Datentypen und Wertebereiche;
* zeitliche Abdeckung von Abfahrt, Ankunft und Ingestion;
* Verteilungen wichtiger numerischer Merkmale;
* Häufigkeiten kategorialer Merkmale;
* fehlende Werte je Spalte;
* Eindeutigkeit und Mehrfachvorkommen technischer IDs.

Erzeugt zusätzlich eine **vorläufige stündliche Fahrtenzahl**. Verwendet diese Sicht nur zur Exploration und bewahrt die Rohdaten auf Zeilenebene.

Formuliert vor der Detailanalyse mindestens drei überprüfbare Hypothesen, zum Beispiel:

* Der Peak stammt von real höherer Nachfrage.
* Der Peak entstand durch ein verspätetes oder wiederholtes Laden von Ereignissen.
* Fehlende Zahlungsinformationen treten zufällig auf.
* Negative Gesamtbeträge sind fehlerhafte Fahrten.

Notiert zu jeder Hypothese, welche Beobachtung sie stützen oder widerlegen würde.

## Teil B: Fehlende Werte

Eine reine `isna().sum()`-Tabelle genügt nicht. Prüft, ob fehlende Werte gemeinsam auftreten und mit anderen Merkmalen zusammenhängen.

Bearbeitet folgende Fragen:

1. Welche Spalten weisen Missingness auf?
2. Treten fehlende Werte in denselben Zeilen gemeinsam auf?
3. Unterscheidet sich die Missingness nach `payment\_type`, Anbieter, Tarifcode oder Zeit?
4. Ist `dropna()` fachlich vertretbar? Welche Population würde dadurch entfernt?
5. Bedeutet «fehlend» hier zwingend «unbekannt», oder kann es auch «nicht anwendbar» bedeuten?

Haltet eine vorläufige Behandlung fest. Ihr müsst fehlende Werte nicht um jeden Preis imputieren.

## Teil C: Exakte Duplikate

Vergleicht mindestens drei Definitionen:

1. vollständig identische Zeilen;
2. gleiche technische ID;
3. identischer fachlicher Payload ohne technische Herkunftsspalten.

Begründet, welche Spalten zum fachlichen Payload gehören. Herkunftsinformationen wie Quelldatei, Batch oder Ingestion-Zeit können zwei technisch verschiedene Datensätze kennzeichnen, obwohl sie dasselbe reale Ereignis beschreiben.

Fragen:

* Wie stark ändern sich die Trefferzahlen je Definition?
* Welche Definition beantwortet die Frage nach doppelten Dateien, Ereignissen oder Fahrten?
* Welche Zeile würdet ihr bei einem Replay behalten und warum?
* Welche Lineage-Information muss erhalten bleiben?

Kennzeichnet Verdachtsfälle zunächst über Flags. Löscht sie nicht stillschweigend.

## Teil D: Toleranzbasierter Dublettenabgleich

Nun sucht ihr nach Datensätzen, die wahrscheinlich dieselbe reale Fahrt beschreiben, aber nicht exakt übereinstimmen. Dieses Vorgehen wird auch **Record Linkage** genannt.

Eine ungefilterte Paarbildung über alle Zeilen ist zu teuer und erzeugt viele Zufallstreffer. Arbeitet deshalb zweistufig:

1. **Blocking:** Bildet kleine Kandidatengruppen über weitgehend stabile Merkmale, beispielsweise Anbieter, Start- und Zielzone sowie ein enges Zeitfenster.
2. **Vergleich:** Bewertet Kandidaten anhand mehrerer Merkmale und fachlicher Toleranzen, etwa Abfahrtszeit, Fahrtdauer, Distanz und Betrag.

Wählt Merkmale, deren zufällige gemeinsame Übereinstimmung relativ unwahrscheinlich ist. Dokumentiert jede Toleranz und testet Grenzfälle.

Fragen:

* Welche Attribute sind stabil genug fürs Blocking?
* Welche Merkmale dürfen geringfügig abweichen?
* Wann entstehen False Positives, etwa bei stark frequentierten Zonen?
* Welche Herkunftsspalten liefern zusätzliche Evidenz für einen Replay?
* Welche Fälle bleiben trotz hoher Ähnlichkeit unklar?

## Teil E: Replay oder Gegenbuchung?

Untersucht Gruppen sehr ähnlicher Datensätze mit positiven und negativen Beträgen. Eine negative Zeile kann eine legitime Gegenbuchung sein und sollte nicht automatisch wie ein technischer Replay behandelt werden.

Entscheidet getrennt für mindestens zwei Analyseziele:

* **Nachfrage:** Wie viele physische Fahrten fanden statt?
* **Umsatz:** Welche finanziellen Ereignisse müssen in die Nettosumme einfliessen?

Beantwortet:

1. Welche Zeilen repräsentieren vermutlich wiederholt geladene Ereignisse?
2. Welche Zeilen bilden ein positives Ereignis und seine Gegenbuchung?
3. Welche Zeilen zählen in der Nachfragesicht?
4. Welche Zeilen zählen in der Umsatzsicht?
5. Welche Fälle würdet ihr in Quarantäne statt in eine automatische Regel geben?

## Arbeit mit ChatGPT

Testet zunächst bewusst einen ungenauen Prompt, beispielsweise:

> Bereinige diesen Datensatz von Duplikaten und fehlenden Werten.

Beobachtet, welche Annahmen die KI selbst ergänzt. Formuliert danach einen verbesserten Prompt mit:

* Analyseziel;
* relevanten Spalten und ihrer Bedeutung;
* Definition von Ereignis versus Fahrt;
* gewünschter Ausgabe als prüfbarer Code;
* Aufforderung, Annahmen und mögliche Fehlklassifikationen zu nennen.

Übernehmt keinen Code, bevor ihr ihn an wenigen bekannten Kandidatengruppen geprüft habt.

## Erwartetes Ergebnis der Gruppe

Am Ende präsentiert jede Gruppe kurz:

* drei zentrale Datenqualitätsbefunde;
* die verwendete Definition exakter Duplikate;
* ihre Blocking- und Toleranzlogik für Near-Duplicates;
* die Trennung von Replay und Gegenbuchung;
* je eine Regel für Nachfrage- und Umsatzsicht;
* mindestens einen ungeklärten Fall;
* eine KI-Antwort, die durch besseren Kontext substanziell verbessert wurde.

## Nach dem Walkthrough

Nach der Besprechung werden eine Musterlösung und ein gemeinsamer Checkpoint unter neuen Dateinamen veröffentlicht. Eure Datei `task.ipynb` bleibt unverändert. Für Aufgabe 2 verwendet ihr danach den bereitgestellten Checkpoint:

```text
data/checkpoints/checkpoint\_01\_resolved\_events.parquet
```

Die detaillierte Erläuterung wird nach der Gruppenphase unter `tasks/01\_data\_quality\_and\_duplicates/released/WALKTHROUGH.md` freigeschaltet.

