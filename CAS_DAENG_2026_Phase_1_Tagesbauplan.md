# CAS DAENG 2026 · Transformation

## Phase 1: Didaktischer Tagesbauplan

**Status:** Entwurf zur Freigabe durch die Kursleitung  
**Hinweis zur Durchführung:** Die aktuelle [Workshop-Übersicht](README.md) beginnt mit [Aufgabe 0 zu Maschinendaten](tasks/00_compatibility_and_integration/README.md). «Block 0» weiter unten bezeichnet den ursprünglich geplanten Einstieg in den Taxifall.
**Umfang:** 9 Lektionen à 45 Minuten = 405 Minuten Netto-Unterrichtszeit  
**Case:** *One row, one ride?* – MetroPulse Operations  
**Basis:** Skript 2025, bestehender Datenprototyp und bisherige didaktische Entscheidungen

> Dieses Dokument ist kursleitungsintern. Es enthält den geplanten
> Erkenntnispfad und Case-Signale, die den Teilnehmenden erst schrittweise
> offengelegt werden.

---

## 1. Ergebnis der Phase 1

Der Transformationstag wird als durchgängige Untersuchung eines realitätsnahen
Datenvorfalls aufgebaut. Die neun Lektionen gliedern sich in **sechs
Case-Blöcke**. Jeder Block kombiniert einen kurzen Theorie-Input, eine
Arbeitsphase in Zweier- oder Dreiergruppen, einen Walkthrough und einen neuen
gesicherten Ausgangspunkt für den nächsten Block.

Die Dramaturgie folgt dieser Kette:

1. Daten verstehen und Hypothesen bilden;
2. Ereigniszeit, Verarbeitungszeit, Kompatibilität und Integration klären;
3. Missingness und exakte Duplikate untersuchen;
4. anspruchsvollere Dubletten und Gegenbuchungen auflösen;
5. statistische Ausreisser von begründetem Noise unterscheiden;
6. zweckabhängige Datenprodukte erzeugen und Rück- sowie Vorhersagen vergleichen.

KI wird nicht als separates Schlusskapitel behandelt. Jeder Block enthält eine
gezielte KI-Anwendung sowie eine typische Fehlanwendung, deren Wirkung anhand
der Daten oder des Codes überprüft wird.

---

## 2. Einordnung des Skripts von 2025

Das bisherige Skript umfasst 103 Folien und acht fachliche Kapitel.

| Kapitel 2025 | Folien | Behandlung 2026 |
| --- | ---: | --- |
| Kombination von Streams mit anderen Daten | 9–12 | Beibehalten und direkt mit Event Time, Ingestion Time und Replay-Ereignissen des Cases verbinden. |
| Verarbeitung im verteilten Setting: MapReduce und Spark | 13–34 | Stark verdichten. Konzepte und Relevanz erklären; kein separater Spark-Programmierblock. |
| Kompatibilitäten | 35–46 | Praktisch in Datentypen, Zeitebenen, Einheiten, abgeleiteten Merkmalen und Referenzdaten anwenden. |
| Integration | 47–52 | Mit Lookup-Tabellen, Join-Kardinalitäten und Validierungen in den Case integrieren. |
| Datenqualität | 53–63 | Als wiederkehrenden Entscheidungsrahmen verwenden; Qualitätsmanagement und Standards kompakt einordnen. |
| Fehlende Daten, Duplikate und Dubletten | 64–72 | Zu zwei aufeinander aufbauenden Case-Blöcken ausbauen. |
| Noise und Ausreisser | 73–93 | Zum analytischen Schwerpunkt mit Statistik, Algorithmus und Domänenrecherche ausbauen. |
| Prognosen über Vergangenheit und Zukunft | 94–100 | Als sichtbaren Nachweis des Nutzens der Transformation abschliessen. |

### Empfohlene inhaltliche Verschiebungen

- MapReduce und Spark bleiben als Orientierungswissen erhalten, werden aber auf
  die für den Case relevanten Konzepte reduziert: verteilte Transformation,
  Shuffle, Lazy Evaluation, Event Time und verspätete Daten.
- OpenRefine wird nicht als zusätzliche Pflichtumgebung installiert. Die
  Bereinigungsaufgaben werden reproduzierbar mit Python umgesetzt. OpenRefine
  kann auf einer Folie als alternative Werkzeugklasse erwähnt werden.
- ISO 8000, Data Governance und der zyklische Bereinigungsprozess werden als
  Entscheidungsrahmen vermittelt, nicht als langer isolierter Theorieblock.
- Der bisherige Wechsel zwischen voneinander unabhängigen Beispieldatensätzen
  entfällt. Alle praktischen Aufgaben arbeiten am selben Case.
- Die Prognose bleibt methodisch bewusst einfach. Im Zentrum steht der Einfluss
  der Transformation auf das Resultat, nicht ein Modellwettbewerb.

---

## 3. Case-Rahmen

### 3.1 Titel und Rollen

**Case-Titel:** *One row, one ride?*  
**Fiktive Organisation:** MetroPulse Operations  
**Reale Datenbasis:** NYC TLC Yellow Taxi Trip Records, Juli 2025

MetroPulse Operations bereitet aus den offiziellen Taxidaten operative
Datenprodukte für Nachfrage, Umsatz und Fahrtdauer auf. Nach einer Änderung an
der Ingestion-Pipeline zeigt das Dashboard an einem Freitagabend einen
auffälligen Nachfrage-Peak. Gleichzeitig soll das Team eine historische Lücke
rekonstruieren und die Nachfrage für die folgende Woche prognostizieren.

Die Teilnehmenden übernehmen die Rolle eines Data-Engineering-Teams. Ihre
Aufgabe lautet nicht einfach «Daten säubern», sondern für jeden Befund zu
entscheiden:

- Was stellt eine Zeile fachlich dar?
- Welche Evidenz spricht für einen Fehler, einen legitimen Sonderfall oder
  einen technischen Replay?
- Welche Behandlung ist für das jeweilige Datenprodukt richtig?
- Wie verändert die Transformation eine nachgelagerte Analyse?

### 3.2 Drei Datenprodukte und eine Quarantäne

| Datenprodukt | Fachlicher Zweck | Zentrale Regelidee |
| --- | --- | --- |
| `trips_for_demand` | Anzahl physischer Fahrten | Replays und negative Gegenbuchungen dürfen keine zusätzliche Fahrt erzeugen. |
| `events_for_revenue` | Finanzielle Ereignisse und Umsatz | Positive und negative Gegenbuchungen bleiben relevant; technische Replays nicht. |
| `trips_for_duration` | Fahrtdauer und Geschwindigkeit | Zeitlich oder physikalisch unplausible Datensätze werden ausgeschlossen; legitime Fernfahrten bleiben erhalten. |
| `quarantined_records` | Nachvollziehbare Prüfmenge | Ausschlüsse werden mit Grund dokumentiert und nicht stillschweigend gelöscht. |

Diese Unterscheidung trägt die zentrale Botschaft des Tages: Es gibt nicht die
eine universelle «Clean Table». Datenqualität ist vom Verwendungszweck
abhängig.

### 3.3 Nachgewiesene Case-Signale

Der vorhandene Prototyp enthält 200’900 Zeilen mit 24 Feldern:

- 200’000 Zeilen aus dem offiziellen TLC-Datensatz;
- 900 kontrollierte Replay-Ereignisse, davon 750 exakte und 150 leicht
  veränderte Kopien;
- 52’540 strukturell fehlende Werteblöcke, vollständig konzentriert auf
  `payment_type = 0`;
- 751 exakte Payload-Kopien, darunter ein nicht kontrollierter Kandidat aus der
  Originalquelle;
- 405 Signaturgruppen mit positivem und negativem Finanzereignis;
- 23’289 univariate IQR-Kandidaten und 1’980 Isolation-Forest-Kandidaten;
- 38 bestätigte physikalisch unmögliche Distanz-/Geschwindigkeitsfälle;
- 32 valide Fernfahrten, die ebenfalls stark statistisch auffallen;
- 6’176 Null-Distanzen und 2’984 nichtpositive Dauern, die nicht pauschal als
  klare Noise-Fälle behandelt werden dürfen;
- drei ungültige Ereigniszeitpunkte und vier valide Monatsgrenzfälle.

Der vorhandene End-to-End-Test zeigt ausserdem:

- Für die historische Lücke ist der Median derselben Wochentagsstunde deutlich
  besser als eine blinde zeitliche Interpolation.
- Bei der saisonal-naiven Wochenprognose sinkt der WAPE von rund 12,14 % auf
  11,36 %, wenn die bereinigte Demand-Sicht anstelle der Rohdaten verwendet
  wird.

Die Zahlen sind kursleitungsintern und werden im Unterricht nur blockweise
aufgelöst.

---

## 4. Lernziele des neuen Tages

Nach dem Transformationstag können die Teilnehmenden:

1. Transformationen im Data-Engineering-Lebenszyklus fachlich einordnen;
2. zwischen fachlichem Ereignis, technischem Ingest-Ereignis und physischer
   Fahrt unterscheiden;
3. formatbedingte, inhaltliche und zeitliche Kompatibilitätsprobleme erkennen
   und Transformationen kontrolliert anwenden;
4. fehlende Werte nach Muster und Quellsemantik beurteilen;
5. exakte Duplikate sowie Near-Duplicates anhand zusammengesetzter Attribute,
   Toleranzen und Lineage untersuchen;
6. statistische Ausreisser als Untersuchungskandidaten behandeln und mit
   Domänenwissen zwischen validen Sonderfällen und Noise unterscheiden;
7. zielabhängige Datenprodukte und eine nachvollziehbare Quarantäne erzeugen;
8. Rück- und Vorhersagen auf Rohdaten und transformierten Daten vergleichen;
9. KI für Analyse und Entwicklung einsetzen, Annahmen sichtbar machen und
   Resultate mit Code, Tests, Stichproben und Fachwissen validieren;
10. explorativen Notebook-Code schrittweise in kleinere Funktionen und
    reproduzierbare Transformationsschritte überführen.

---

## 5. Übergreifende didaktische Regeln

### 5.1 Arbeitsrhythmus pro Block

Jeder Block folgt demselben Muster:

1. **Input:** Konzept, fachlicher Auftrag und verfügbare Evidenz;
2. **Explore:** Gruppen untersuchen Daten und formulieren eine Entscheidung;
3. **Explain:** Gruppen begründen Ergebnis, Unsicherheit und offene Fragen;
4. **Walkthrough:** Kursleitung demonstriert einen belastbaren Lösungsweg;
5. **Checkpoint:** geprüfter Ausgangspunkt für den nächsten Block wird
   freigegeben.

### 5.2 Entscheidungslog als roter Faden

Jede Gruppe führt während des ganzen Tages ein Entscheidungslog mit fünf
Feldern:

| Feld | Leitfrage |
| --- | --- |
| Beobachtung | Was sehen wir tatsächlich in den Daten? |
| Hypothese | Welche Erklärung könnte dazu passen? |
| Evidenz | Welche Abfrage, Visualisierung oder Quelle stützt die Erklärung? |
| Entscheidung | Behalten, transformieren, zusammenführen, ausschliessen oder prüfen? |
| Geltungsbereich | Für welches Datenprodukt gilt diese Entscheidung? |

### 5.3 Gruppenorganisation

Für zehn Teilnehmende werden vier stabile Gruppen empfohlen:

- zwei Dreiergruppen;
- zwei Zweiergruppen.

Die Rollen wechseln nach jedem Block:

- **Operator:** führt Code und Abfragen aus;
- **Reviewer:** hinterfragt Annahmen und prüft Ergebnisse;
- **Reporter:** dokumentiert Entscheidung und Evidenz.

In Zweiergruppen werden Reviewer und Reporter kombiniert. Stabile Gruppen
erleichtern den Aufbau einer konsistenten Case-Theorie; der Rollenwechsel
verhindert, dass nur eine Person programmiert.

---

## 6. Ablauf der neun Lektionen

Die Zeitangaben summieren sich pro Lektion auf 45 Minuten. Die fünf Minuten
Reserve dienen Wechseln, technischen Verzögerungen und kurzen Rückfragen.
Pausen sind nicht Teil der 405 Minuten. Sinnvolle Einschnitte liegen nach den
Lektionen 2 und 7 sowie – abhängig vom Stundenplan – zwischen den Lektionen 4
und 5.

| Lektion | Schwerpunkt | Input | Gruppenarbeit | Walkthrough | Reserve |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | Case-Start, Datenvertrag, EDA und Hypothesen | 12 min | 18 min | 10 min | 5 min |
| 2 | Streams, verteilte Transformation und Replay-Story | 15 min | 17 min | 8 min | 5 min |
| 3 | Kompatibilität, Integration und abgeleitete Merkmale | 12 min | 20 min | 8 min | 5 min |
| 4 | Datenqualität, Missingness und exakte Duplikate | 10 min | 22 min | 8 min | 5 min |
| 5 | Near-Duplicates, Signaturen und Gegenbuchungen | 10 min | 22 min | 8 min | 5 min |
| 6 | Verteilungen, Boxplots und univariate Ausreisser | 10 min | 22 min | 8 min | 5 min |
| 7 | Multivariate Kandidaten, Recherche und Noise-Entscheid | 10 min | 22 min | 8 min | 5 min |
| 8 | Ziel-Views, Modularisierung und Rückschätzung | 13 min | 19 min | 8 min | 5 min |
| 9 | Zukunftsprognose, Managemententscheid und KI-Retrospektive | 10 min | 20 min | 10 min | 5 min |

---

## 7. Detaillierter Case- und Aufgabenverlauf

### Block 0 · Case Intake und Hypothesen

**Lektion:** 1  
**Vorgesehener Ordner:** `tasks/00_case_intake/`

**Input**

- Transformation als Wertschöpfung im Data-Engineering-Lebenszyklus;
- Managementauftrag von MetroPulse Operations;
- Datenvertrag und Bedeutung der 24 Ausgangsfelder;
- Unterschied zwischen Beobachtung und Interpretation.

**Gruppenauftrag**

Die Gruppen erstellen ein erstes Profil und formulieren überprüfbare
Hypothesen zu:

- fehlenden Werten;
- ungewöhnlichen Zeitbereichen;
- möglichen Duplikaten;
- Distanz, Dauer und Gesamtbetrag;
- auffälligen Nachfrageperioden.

Jede Gruppe priorisiert drei Hypothesen und notiert, welche Evidenz zur Prüfung
benötigt wird.

**Story-Reveal**

Der Datensatz enthält 200’900 Zeilen, aber die Gleichung «eine Zeile = eine
Fahrt» ist noch nicht belegt. Der Pickup-Zeitbereich enthält zudem einzelne
unerwartete historische Werte.

**KI-Fokus**

- ChatGPT erzeugt aus einem unspezifischen Auftrag eine generische Liste von
  Datenqualitätsproblemen.
- Danach erhält ChatGPT Datenvertrag, Managementziel und gewünschte Form einer
  testbaren Hypothese.
- Verglichen werden Spezifität, Annahmen, erfundene Spalten und tatsächliche
  Prüfbarkeit.

**Freigabe nach dem Walkthrough**

- Walkthrough und Musterlösung;
- kein Datencheckpoint erforderlich, weil noch keine Transformation verbindlich
  angewendet wurde.

### Block 1 · Event Time, Processing Time, Kompatibilität und Integration

**Lektionen:** 2–3  
**Vorgesehener Ordner:** `tasks/01_event_time_and_integration/`

**Input Lektion 2**

- Tabellen-Join, Enrichment und Stream-to-Stream-Join;
- Event Time gegenüber Ingestion/Processing Time;
- verspätete Daten, Watermarks, Idempotenz und Replay;
- MapReduce und Spark als kompakter konzeptioneller Rahmen für verteilte
  Transformationen.

**Gruppenauftrag Lektion 2**

Die Gruppen untersuchen `source_file`, `batch_id`, `ingested_at` und
`tpep_pickup_datetime`. Sie beantworten:

- Welche Zeit beschreibt das Ereignis, welche die Verarbeitung?
- Welche Dateien und Batches sind vorhanden?
- Ist ein später eingetroffener Datensatz automatisch eine neue Fahrt?
- Welche zusätzliche Evidenz wäre für einen Replay nötig?

**Story-Reveal Lektion 2**

900 Ereignisse aus dem Zeitfenster Freitag, 18. Juli, 17:00–21:00 Uhr wurden am
Montag, 21. Juli, erneut eingespielt. Noch ist nicht geklärt, ob alle 900
identische Kopien sind.

**Input und Gruppenauftrag Lektion 3**

- Datentypen, Einheiten und zeitliche Granularität prüfen;
- `duration_min` und `speed_mph` ableiten;
- Zonen-, Tarif- und Zahlungsarten-Lookups integrieren;
- Join-Kardinalität, Zeilenzahl und nicht zugeordnete Schlüssel validieren.

**Story-Reveal Lektion 3**

Die Referenzdaten schaffen später die fachliche Evidenz für Outside-of-NYC- und
Negotiated-Fare-Fahrten. Ein erfolgreicher Join wird nicht nur durch ausführbaren
Code, sondern auch durch stabile Zeilenzahl und erwartete Kardinalität belegt.

**KI-Fokus**

- Claude Code erhält zunächst nur den Auftrag «Analysiere und verbessere die
  Repo». Die Gruppe identifiziert unklaren Scope und potenziell unnötige
  Änderungen.
- Im zweiten Versuch darf Claude Code nur definierte Dateien lesen, einen Plan
  vorschlagen und noch nichts verändern.
- Beim Join wird demonstriert, wie KI ohne Kardinalitätsanforderung eine
  Zeilenvervielfachung erzeugen kann.

**Checkpoint**

`data/checkpoints/checkpoint_01_enriched.parquet`

### Block 2 · Missingness und exakte Duplikate

**Lektion:** 4  
**Vorgesehener Ordner:** `tasks/02_basic_data_quality/`

**Input**

- Datenqualitätsdimensionen und zyklischer Bereinigungsprozess;
- standardisierte und nicht standardisierte Missing Values;
- MCAR, MAR und MNAR als Orientierung, ohne vertiefte Statistik;
- technisches Duplikat gegenüber identischem fachlichem Payload.

**Gruppenauftrag**

1. Fehlende Werte pro Spalte und gemeinsame Nullmuster bestimmen.
2. Missingness nach `payment_type` aufschlüsseln.
3. Exakte Duplikate einmal über alle Spalten und einmal nur über die fachlichen
   Quellfelder suchen.
4. Für jeden Befund eine Behandlung und einen Geltungsbereich festlegen.

**Story-Reveal**

- Der Nullblock mit 52’540 Zeilen ist vollständig an `payment_type = 0` und
  damit an eine Quellsemantik gebunden. Ein pauschales `dropna()` wäre falsch.
- Die technischen Metadaten verhindern, dass Replays bei einem Vergleich über
  alle Spalten erkannt werden.
- Es existieren 751 exakte Payload-Kopien; 750 stammen aus dem kontrollierten
  Replay, ein Fall bleibt zunächst Kandidat.

**KI-Fokus**

- Negativprompt: «Bereinige den Datensatz vollständig.»
- Erwartbarer Fehlweg: `dropna()` und `drop_duplicates()` ohne Teilmenge,
  Zweck oder Vorher-nachher-Prüfung.
- Verbesserter Auftrag: Qualitätsziel, geschützte Fälle, Vergleichsspalten,
  gewünschtes Entscheidungslog und Akzeptanztests explizit nennen.

**Checkpoint**

`data/checkpoints/checkpoint_02_basic_quality.parquet`

### Block 3 · Near-Duplicates und Ereignissemantik

**Lektion:** 5  
**Vorgesehener Ordner:** `tasks/03_record_linkage/`

**Input**

- Duplikat, Dublette und Record Linkage;
- zusammengesetzte Signaturen aus gemeinsam seltenen Attributen;
- Blocking, toleranzbasierte Vergleiche und Lineage;
- physische Fahrt gegenüber finanziellem Ereignis.

**Gruppenauftrag**

1. Eine fachliche Signatur ohne technische Metadaten und zunächst ohne
   Finanzbeträge definieren.
2. Mehrfachsignaturen untersuchen.
3. Replay-Kandidaten über diskrete Attribute blocken und Zeit, Distanz sowie
   Betrag innerhalb begründeter Toleranzen vergleichen.
4. Positive/negative Paare für Demand und Revenue unterschiedlich beurteilen.

**Story-Reveal**

- Die 150 veränderten Replay-Zeilen unterscheiden sich nur minimal in Zeit,
  Distanz oder Betrag.
- 405 Signaturgruppen sind keine technischen Kopien, sondern bestehen aus
  positiven und negativen Finanzereignissen.
- Für Demand darf eine Gegenbuchung keine zusätzliche Fahrt erzeugen; für
  Revenue müssen beide Ereignisse erhalten bleiben.

**KI-Fokus**

- Claude Code soll zunächst ohne weitere Anforderungen «fuzzy duplicates»
  finden. Erwartbare Probleme sind ein kartesischer Vergleich, willkürliche
  Gewichte und nicht begründete Schwellenwerte.
- Der verbesserte Auftrag verlangt Blocking, nachvollziehbare Toleranzen,
  Laufzeitgrenze, Stichprobenprüfung und Tests mit bekannten Paaren und
  Nicht-Paaren.

**Checkpoint**

`data/checkpoints/checkpoint_03_resolved_events.parquet`

### Block 4 · Ausreisser, Noise und Domänenbegründung

**Lektionen:** 6–7  
**Vorgesehener Ordner:** `tasks/04_outliers_and_noise/`

**Input Lektion 6**

- Verteilungen, Quantile, IQR und Tukey-Boxplot;
- Ausreisser als statistische Definition, nicht als Fehlerlabel;
- abgeleitete Merkmale `duration_min` und `speed_mph`;
- konkurrierende Erklärungen für lange Distanzen.

**Gruppenauftrag Lektion 6**

Die Gruppen bestimmen univariate Kandidaten, untersuchen Extremwerte und
formulieren mindestens zwei konkurrierende Erklärungen. Sie vergleichen
Distanz, Dauer, Geschwindigkeit, Tarifcode und Zielzone.

**Zwischen-Reveal**

Die IQR-Grenze für `trip_distance` liegt bei rund 8,22 Meilen und markiert über
23’000 Datensätze. Darunter befinden sich sowohl physikalisch unmögliche Werte
als auch reale Fernfahrten. Die Kandidatenzahl ist deshalb keine Löschliste.

**Input Lektion 7**

- Isolation Forest als multivariate Priorisierung;
- Einfluss von Features, Skalierung und `contamination`;
- fachliche Recherche und Referenzdaten als Evidenz;
- Quarantäne, Unsicherheit und regelbasierter Entscheid.

**Gruppenauftrag Lektion 7**

1. Isolation-Forest-Kandidaten erzeugen und mit den IQR-Kandidaten vergleichen.
2. Eine kleine Review-Tabelle mit Befund, Evidenz, Konfidenz und Massnahme
   erstellen.
3. Regeln für klare Noise-Fälle formulieren.
4. Ambivalente Null-Distanzen und nichtpositive Dauern bewusst von bestätigtem
   Noise trennen.

**Story-Reveal**

- 38 Fahrten kombinieren grosse Distanz mit physikalisch unmöglicher
  Geschwindigkeit.
- 32 sehr lange Fahrten sind mit Tarifcode, Dauer, Geschwindigkeit und
  Outside-of-NYC-Ziel plausibel.
- Drei Ereigniszeitpunkte sind ungültig.
- Isolation Forest und IQR liefern Kandidaten, aber keine Ground Truth.

**KI-Fokus**

- ChatGPT interpretiert zunächst eine Kandidatenliste ohne Datenvertrag und
  empfiehlt, alle Ausreisser zu entfernen.
- Im verbesserten Ablauf muss das Modell alternative Erklärungen, benötigte
  Domäneninformationen und überprüfbare Regeln nennen.
- Die Anaconda Online Toolbox kann optional als Negativvergleich für einen
  unter-spezifizierten Cloud-Workflow dienen. Gezeigt wird nicht «ein schlechtes
  Produkt», sondern ein schlechter Prozess: fehlender Repo-Kontext, generische
  Bereinigung, unklare Paketversionen und ungeprüfte Übernahme von Code. Die
  genaue Produktbezeichnung und der Funktionsumfang werden vor der Umsetzung
  nochmals verifiziert.

**Checkpoint**

`data/checkpoints/checkpoint_04_reviewed_records.parquet`

### Block 5 · Ziel-Views, Rückschätzung und Zukunftsprognose

**Lektionen:** 8–9  
**Vorgesehener Ordner:** `tasks/05_views_and_forecasting/`

**Input Lektion 8**

- zielabhängige Transformationsregeln;
- Demand-, Revenue-, Duration- und Quarantäne-Sicht;
- Aggregation auf stündliche Granularität;
- historische Lücke als Rückschätzungsaufgabe.

**Gruppenauftrag Lektion 8**

1. Transformationsentscheidungen aus dem Entscheidungslog den vier Views
   zuordnen.
2. Die stündliche Demand-Zeitreihe erstellen.
3. Den 10. Juli maskieren und drei Baselines vergleichen:
   Zeitinterpolation, Median derselben Wochentagsstunde und lineares
   Kalendermodell.
4. Annahmen und Fehlermetriken dokumentieren.

**Story-Reveal Lektion 8**

Eine einfache Interpolation über 24 Stunden bildet den Tagesrhythmus nicht ab.
Der Median derselben Stunde an vergleichbaren Wochentagen liefert im Prototyp
die deutlich bessere Rückschätzung.

**Code- und KI-Demonstration**

- Einen gewachsenen Notebook-Abschnitt in kleine Funktionen für Feature-Bau,
  View-Erzeugung und Fehlermetriken überführen.
- Claude Code zuerst einen Plan und Tests vorschlagen lassen, danach nur eine
  kleine, überprüfbare Änderung erlauben.
- In VS Code Diff, Funktionsgrenzen und Testausführung zeigen.
- Marimo optional für 10–12 Minuten nutzen, um reaktive Abhängigkeiten und
  versteckten Notebook-Zustand sichtbar zu machen. Falls Marimo praktisch
  ausgeführt wird, muss die Abhängigkeit in Phase 3 in die Umgebung aufgenommen
  und erneut in Codespaces getestet werden.

**Checkpoint**

`data/checkpoints/checkpoint_05_hourly_demand.parquet`

**Input und Gruppenauftrag Lektion 9**

- Zukunftsprognose für den 25.–31. Juli;
- saisonal-naive Wochenprognose und lineares Kalendermodell;
- Rohsicht gegenüber bereinigter Demand-Sicht;
- MAE und WAPE sowie Grenzen der Aussage.

Die Gruppen formulieren abschliessend eine Managementempfehlung:

- Was verursachte den auffälligen Freitagabend?
- Welche Daten wurden ausgeschlossen und weshalb?
- Wie stark verändert die Bereinigung die Prognose?
- Welche Unsicherheiten und Monitoring-Massnahmen bleiben?

**Finales Reveal**

Der Replay-Peak wird von der saisonal-naiven Prognose aus der Rohsicht eine
Woche weitergetragen. Die bereinigte Demand-Sicht reduziert den Fehler. Die
Verbesserung ist sichtbar, aber nicht gross genug für eine übertriebene
Kausalitäts- oder Modellgütebehauptung.

**KI-Fokus**

- ChatGPT und Claude erhalten dieselben Resultate und sollen eine
  Managementzusammenfassung formulieren.
- Geprüft werden erfundene Ursachen, übertriebene Sicherheit, selektive
  Metrikdarstellung und fehlende Einschränkungen.
- Abschlussfrage: Welche Teile wurden durch KI beschleunigt, und welche
  Entscheidungen blieben menschliche Verantwortung?

**Freigabe nach dem Walkthrough**

- vollständiger Walkthrough;
- Musterlösung;
- finales Entscheidungslog;
- kein weiterer Datencheckpoint erforderlich.

---

## 8. Freigabe- und Checkpoint-Architektur

| Block | Startpunkt | Freigabe nach Walkthrough | Ausgangspunkt des Folgeblocks |
| --- | --- | --- | --- |
| 0 Case Intake | `data/input/trips_case_initial.parquet` | Walkthrough + Musterlösung | unveränderte Inputdaten |
| 1 Event Time & Integration | Inputdaten | Walkthrough + Musterlösung + `checkpoint_01_enriched.parquet` | Checkpoint 01 |
| 2 Basic Data Quality | Checkpoint 01 | Walkthrough + Musterlösung + `checkpoint_02_basic_quality.parquet` | Checkpoint 02 |
| 3 Record Linkage | Checkpoint 02 | Walkthrough + Musterlösung + `checkpoint_03_resolved_events.parquet` | Checkpoint 03 |
| 4 Outliers & Noise | Checkpoint 03 | Walkthrough + Musterlösung + `checkpoint_04_reviewed_records.parquet` | Checkpoint 04 |
| 5 Views & Forecasting | Checkpoint 04 | Zwischencheckpoint 05 nach Lektion 8; finale Lösung nach Lektion 9 | Abschluss |

Die `task.ipynb`-Dateien werden nach Workshopbeginn nicht verändert.
Walkthroughs, Musterlösungen und Checkpoints kommen immer unter neuen Namen
hinzu. Dadurch bleiben eigene Lösungen bei Sync und Pull erhalten.

---

## 9. KI-Curriculum über den Tag

### 9.1 Einheitliches Arbeitsprotokoll

Jede KI-Aufgabe verwendet dieselben sieben Schritte:

1. Ziel und fachlichen Verwendungszweck nennen;
2. relevanten Kontext und zulässige Dateien eingrenzen;
3. Annahmen und offene Fragen explizit verlangen;
4. zuerst Analyse oder Plan, danach eine kleine Änderung;
5. Ergebnis über Daten, Stichproben, Diff und Tests prüfen;
6. Fehler oder unklare Entscheidungen dokumentieren;
7. erst danach Code übernehmen und committen.

### 9.2 Geplante Stärken und Schwächen

| Block | Stärke der KI | Gezielte Schwäche bzw. Fehlanwendung |
| --- | --- | --- |
| Case Intake | Hypothesen und Analyseideen strukturieren | generische Antworten, erfundene Spalten, fehlender Datenbezug |
| Event Time & Integration | Repo und Codepfade erklären, Transformationsplan entwerfen | zu grosser Scope, unkontrollierte Änderungen, falsche Join-Kardinalität |
| Basic Data Quality | Profiling-Code und Tests vorschlagen | blindes `dropna()` und `drop_duplicates()` |
| Record Linkage | Blocking und Matching-Code modularisieren | quadratische Vergleiche, magische Schwellenwerte, fehlende Negativtests |
| Outliers & Noise | alternative Erklärungen und Review-Kriterien sammeln | statistischer Ausreisser wird ohne Evidenz zum Fehler erklärt |
| Views & Forecasting | Refactoring, Tests und Ergebnistext unterstützen | Data Leakage, Metrik-Cherry-Picking und übertriebene Kausalität |

### 9.3 Dokumentation in jeder Aufgabe

Jede Aufgabe erhält eine kurze KI-Reflexionsbox:

- verwendetes System und Prompt;
- nützlicher Beitrag;
- problematische oder falsche Aussage;
- durchgeführte Prüfung;
- übernommene oder verworfene Änderung.

Die Bewertung richtet sich nicht danach, ob KI verwendet wurde, sondern ob der
Output nachvollziehbar geprüft wurde.

---

## 10. Dateien, die erst nach Freigabe dieses Plans entstehen

Noch nicht erstellen:

- Teilnehmenden-Notebooks der sechs Blöcke;
- Walkthroughs und Musterlösungen;
- Referenz- und Lookup-Tabellen;
- fünf Checkpoints;
- Marimo-Beispiel;
- KI-Promptkarten;
- Workshop-Landingpage und Navigation.

Diese Dateien werden erst aus dem freigegebenen Case Blueprint und der
Ground Truth in Phase 2 abgeleitet.

---

## 11. Entscheidungen für die Freigabe von Phase 1

Die Kursleitung bestätigt oder ändert folgende Punkte:

1. MapReduce/Spark werden auf einen konzeptionellen Input in Lektion 2
   verdichtet; es gibt keine Spark-Programmieraufgabe.
2. OpenRefine wird nicht als Pflichtumgebung eingesetzt.
3. Der Tag verwendet sechs Case-Blöcke und fünf Datencheckpoints.
4. Die vier Gruppen bleiben über den Tag stabil; die Rollen rotieren.
5. Der Case-Name *One row, one ride?* und MetroPulse Operations bleiben
   bestehen.
6. Marimo wird als kurze optionale Demonstration in Lektion 8 eingeplant.
7. Der Anaconda-Online-Vergleich demonstriert einen problematischen Workflow,
   nicht pauschal ein problematisches Produkt.
8. Die Prognosemethoden bleiben bewusst einfach, damit der Cleaning-Effekt im
   Zentrum steht.

Nach Freigabe dieser acht Entscheidungen beginnt Phase 2 mit dem detaillierten
Case Blueprint, dem Reveal-Plan und der verbindlichen Ground-Truth-Matrix.
