[Workshop-Übersicht](../../README.md) · [Technische Vorbereitung](../../README_technical_preparation.md) · [Aufgabe 0: Kompatibilität und Integration](../00_compatibility_and_integration/README.md) · [Aufgabe 1: Datenqualität und Dubletten](../01_data_quality_and_duplicates/README.md) · [Aufgabe 2: Ausreisser und Noise](../02_outliers_and_noise/README.md) · [Aufgabe 3: Rückschätzung und Prognose](../03_forecasting/README.md)

---

# Aufgabe 3: Rückschätzung, Prognose und Managementaussage

[Zur Workshop-Übersicht](../../workshop/README.md)

In den letzten Lektionen habt ihr gesehen, wie Transformationen in kleine, testbare Funktionen zerlegt und zweckspezifische Datenprodukte erzeugt werden. Nun prüft ihr, welchen Unterschied die Datenbereinigung für Rückschätzung und Prognose macht.

## Ausgangslage

MetroPulse Operations benötigt eine stündliche Nachfrageprognose. Das Management fragt zugleich, ob die bereinigten Daten tatsächlich bessere Entscheidungen ermöglichen oder nur weniger Beobachtungen enthalten.

Ihr erstellt deshalb zwei Vergleiche:

* eine **Rückschätzung** für einen bekannten Zeitraum innerhalb des beobachteten Monats;
* eine **Zukunftsprognose** für die folgende Woche, deren Istwerte erst im Walkthrough offengelegt werden.

## Dateien

Gemeinsamer Ausgangspunkt nach Aufgabe 2:

```text
data/checkpoints/checkpoint\_02\_reviewed\_quality.parquet
```

Arbeitsnotebook:

```text
tasks/03\_forecasting/task.ipynb
```

Die Kursleitung stellt bei Bedarf ein Funktionsgerüst für zweckspezifische Sichten, stündliche Aggregation und Evaluation bereit.

## Lernziele

Nach der Aufgabe könnt ihr:

* aus dokumentierten Qualitätsentscheidungen eine Nachfragesicht ableiten;
* eine vollständige stündliche Zeitreihe mit expliziten Nullstunden erzeugen;
* ein Backtesting-Szenario ohne Leakage aufbauen;
* einfache Baselines gegen ein erweitertes Modell vergleichen;
* MAE und WAPE korrekt interpretieren;
* den Einfluss der Bereinigung von Modellwahl und Zufallsschwankung trennen;
* Resultate adressatengerecht und mit Unsicherheit kommunizieren.

## Teil A: Zweckspezifische Nachfragesicht

Erstellt eine Sicht, in der jede berücksichtigte Zeile einer physischen Fahrt entspricht. Verwendet die Flags und Entscheidungen aus den Checkpoints. Begründet insbesondere:

* welche Replay-Ereignisse nicht erneut gezählt werden;
* wie Gegenbuchungen in der Nachfragesicht behandelt werden;
* welche klaren Noise-Fälle ausgeschlossen werden;
* welche mehrdeutigen Fälle enthalten bleiben oder separat ausgewiesen werden.

Vergleicht mindestens eine rohe und eine bereinigte Variante. Der Vergleich soll mit denselben Zeitgrenzen und derselben Aggregationslogik erfolgen.

## Teil B: Vertrauenswürdige stündliche Aggregation

Aggregiert die Abfahrten auf vollständige Stunden. Achtet auf:

* eindeutig gewählte Zeitspalte;
* sortierten Zeitindex;
* vollständiges stündliches Raster;
* explizite Behandlung von Stunden ohne beobachtete Fahrt;
* keine Information aus der Zukunft bei Feature-Erzeugung oder Imputation.

Vergleicht die endgültige Serie mit der explorativen Aggregation aus Aufgabe 1. Erklärt, weshalb die Aggregation nun belastbarer ist und welche Information auf Zeilenebene trotzdem erhalten bleiben muss.

## Teil C: Rückschätzung eines historischen Zeitraums

Behandelt den von der Kursleitung genannten Kalendertag innerhalb des Trainingszeitraums so, als wären seine Werte unbekannt. Entfernt diesen Zeitraum aus den Trainingsdaten und schätzt ihn mit mindestens zwei Verfahren:

1. einer einfachen Referenzmethode, beispielsweise Interpolation;
2. einer saisonalen Baseline, beispielsweise Median vergleichbarer Wochentag-Stunden.

Optional ergänzt ihr ein lineares Kalendermodell oder ein anderes einfach erklärbares Verfahren.

Wichtig: Für die Rückschätzung dürft ihr die echten Werte erst zur Evaluation verwenden. Prüft euren Code auf Leakage.

Berechnet mindestens:

\[
MAE = \\frac{1}{n}\\sum\_{t=1}^{n}|y\_t-\\hat{y}\_t|
]

\[
WAPE = \\frac{\\sum\_{t=1}^{n}|y\_t-\\hat{y}*t|}{\\sum*{t=1}^{n}|y\_t|}
]

Vergleicht rohe und bereinigte Daten. Welches Verfahren ist robust gegenüber einem lokalen Peak, und weshalb?

## Teil D: Zukunftsprognose

Prognostiziert die stündliche Nachfrage für den bereitgestellten Zukunftszeitraum. Verwendet mindestens:

* eine saisonal-naive Prognose, zum Beispiel den Wert derselben Stunde eine Woche zuvor;
* ein einfaches erweitertes Modell mit erklärbaren Kalendermerkmalen.

Die tatsächlichen Werte des Zukunftszeitraums bleiben während der Gruppenarbeit verborgen. Erstellt deshalb vor der Auflösung:

* eine Prognosetabelle mit Zeitstempel und Modellname;
* eine Visualisierung der historischen und prognostizierten Nachfrage;
* Plausibilitätschecks für negative Werte, Lücken und unrealistische Sprünge;
* eine kurze Erwartung, welches Modell nach Offenlegung besser abschneiden dürfte.

Im Walkthrough werden die Istwerte ergänzt und die Modelle mit MAE und WAPE bewertet.

## Teil E: Managementinterpretation

Formuliert eine Nachricht von höchstens sechs Sätzen an das Management. Sie soll enthalten:

* welche Datenprobleme die Nachfragezählung beeinflussten;
* ob die Bereinigung die Rückschätzung beziehungsweise Prognose verbesserte;
* welche Methode empfohlen wird;
* welche Unsicherheit oder Einschränkung bestehen bleibt;
* welche nächste betriebliche Massnahme sinnvoll ist.

Vermeidet unbelegte Kausalität. Aus «Peak und Replay treten gleichzeitig auf» folgt nicht automatisch eine vollständige technische Ursachenanalyse.

## KI-Vergleich: ChatGPT und Claude Code

Gebt ChatGPT und Claude Code dieselben kompakten Ergebnisse: Problemdefinition, verwendete Sicht, Kennzahlen und bekannte Einschränkungen. Lasst beide Systeme eine Managementzusammenfassung erstellen.

Vergleicht:

* Werden Kennzahlen korrekt wiedergegeben?
* Wird Korrelation als Ursache dargestellt?
* Werden Unsicherheiten genannt oder erfunden?
* Wird das beste Modell anhand einer transparenten Regel gewählt?
* Ändert das System Code ausserhalb des beauftragten Bereichs?

Bei Claude Code kontrolliert ihr den Diff, bevor ihr Änderungen übernehmt. Verwendet Tests oder kleine Kontrollbeispiele für modularisierte Funktionen. Die KI-Retrospektive soll nicht nur bewerten, welcher Text besser klingt, sondern welcher Prozess nachvollziehbarer und sicherer war.

## Erwartetes Ergebnis der Gruppe

Am Ende präsentiert jede Gruppe:

* Definition der Nachfragesicht;
* rohe und bereinigte stündliche Zeitreihe;
* Backcast mit mindestens zwei Verfahren und beiden Kennzahlen;
* Zukunftsprognose mit mindestens zwei Verfahren;
* Plausibilitätschecks und erwartete Modellrangfolge;
* Managementnachricht;
* zwei konkrete Best Practices und zwei Risiken beim KI-Einsatz.

## Nach dem Walkthrough

Nach der gemeinsamen Auflösung werden die tatsächlichen Zukunftswerte, die vollständige Evaluation, eine Musterlösung und `tasks/03\_forecasting/released/WALKTHROUGH.md` unter neuen Dateinamen bereitgestellt. Eure Datei `task.ipynb` bleibt erhalten.

