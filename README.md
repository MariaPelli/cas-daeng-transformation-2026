[Workshop-Übersicht](README.md) · [Technische Vorbereitung](README_technical_preparation.md) · [Aufgabe 1: Datenqualität und Dubletten](tasks/01_data_quality_and_duplicates/README.md) · [Aufgabe 2: Ausreisser und Noise](tasks/02_outliers_and_noise/README.md) · [Aufgabe 3: Rückschätzung und Prognose](tasks/03_forecasting/README.md)

---

# Workshop: «One row, one ride?»

Dieser Workshop begleitet den Transformationstag im CAS Data Engineering. Wir arbeiten den ganzen Tag an einem zusammenhängenden Fall: Aus Rohdaten entsteht schrittweise eine belastbare Entscheidungsgrundlage für Betrieb und Management.

Die [technische Vorbereitung](README_technical_preparation.md) beschreibt die Einrichtung für lokale Arbeit und GitHub Codespaces. Diese Seite beschreibt den fachlichen Einstieg und den Ablauf des Workshops.

## Der Fall

**MetroPulse Operations** betreibt eine Analyseplattform für Mobilitätsdaten. Das Management möchte wissen:

- Wie viele Fahrten fanden tatsächlich statt?
- Welche Umsätze gehören in die Finanzsicht?
- Welche ungewöhnlichen Beobachtungen sind echte Extremfälle und welche sind Mess- oder Verarbeitungsfehler?
- Wie hätte sich eine historische Datenlücke plausibel schliessen lassen?
- Wie gut lässt sich die Nachfrage für die folgende Woche prognostizieren?

Als reale Datengrundlage dienen öffentlich verfügbare **NYC TLC Yellow Taxi Trip Records vom Juli 2025**. Für den Unterricht wurde daraus ein reproduzierbarer Case erstellt und um kontrollierte Datenprobleme ergänzt. MetroPulse Operations und die interne Systemgeschichte sind fiktiv; die zugrunde liegenden Taxidaten sind real.

Die Leitfrage lautet:

> Bedeutet eine Zeile immer genau eine reale Fahrt?

Schon früh werden wir sehen, weshalb zwischen **Datensatzzeile**, **technischem Ereignis**, **finanzieller Buchung** und **physischer Fahrt** unterschieden werden muss.

## Incident Briefing

Am Montagmorgen meldet das Operations-Team nach einem Pipeline-Neustart einen ungewöhnlichen Ausschlag im Dashboard. Der Ausschlag betrifft nicht nur die aktuelle Ingestion-Zeit, sondern scheinbar auch Fahrten eines früheren Freitags. Gleichzeitig weicht die Umsatzsicht von der einfachen Fahrtenzählung ab. In den Daten finden sich zudem leere Fahrtdetails, negative Beträge und Distanzen, die von null bis weit ausserhalb des Erwartbaren reichen.

Die Geschäftsleitung setzt drei Leitplanken:

- Die Tagesanalyse muss bis zum Abend reproduzierbar sein.
- Auffällige Zeilen dürfen nicht ohne Begründung verschwinden.
- Nachfrage, Umsatz und Prognose müssen fachlich getrennt betrachtet werden.

Ihr übernehmt die Rolle des Data-Engineering-Teams. Im Laufe des Tages erhaltet ihr schrittweise mehr Evidenz, aber keine fertige «Clean»-Definition.

## Arbeitsweise

Ihr arbeitet in Zweier- oder Dreiergruppen. Jede Gruppe führt ein kurzes **Decision Log**. Haltet darin nicht nur Code, sondern auch Entscheidungen und Begründungen fest:

1. Welche Beobachtung habt ihr gemacht?
2. Welche Hypothesen kommen als Erklärung infrage?
3. Welche Evidenz stützt oder widerlegt diese Hypothesen?
4. Welche Behandlung wählt ihr für welchen Analysezweck?
5. Welche Unsicherheit bleibt bestehen?

Nach jeder Gruppenphase folgt ein gemeinsamer Walkthrough. Anschliessend werden neue Dateien mit **neuen Dateinamen** veröffentlicht, zum Beispiel `task_sample_solution.ipynb` und `WALKTHROUGH.md`. Eure Datei `task.ipynb` wird dadurch nicht überschrieben.

## Tagesablauf in neun Lektionen

| Lektion | Format | Schwerpunkt |
|---:|---|---|
| 1 | Vorlesung | Transformation, Integration, Kompatibilität sowie ein kompakter Blick auf Streams und verteilte Verarbeitung |
| 2 | Vorlesung | Datenqualität, Missingness, exakte Duplikate und toleranzbasierter Dublettenabgleich |
| 3 | Case und Start Gruppenarbeit | Case-Einführung, OpenRefine-Demo, Jupyter-Demo und Beginn von Aufgabe 1 |
| 4 | Gruppenarbeit und Walkthrough | EDA, Hypothesen, Missingness, Duplikate, Near-Duplicates, Replays und Gegenbuchungen |
| 5 | Vorlesung | Noise, Ausreisser, Verteilungen und IQR |
| 6 | Vorlesung | Multivariate Anomalien und Isolation Forest |
| 7 | Gruppenarbeit und Walkthrough | Valide Extremfälle, klare Fehler und begründet unklare Fälle |
| 8 | Demo und Vorlesung | Modularisierung, zweckspezifische Datenprodukte und Prognosen |
| 9 | Gruppenarbeit und Walkthrough | Rückschätzung, Zukunftsprognose, Managementinterpretation und KI-Retrospektive |

## Die drei Aufgaben

1. [Datenqualität und Dubletten](tasks/01_data_quality_and_duplicates/README.md)  
   Vom ersten Profiling bis zur Unterscheidung von Replay-Ereignissen und finanziellen Gegenbuchungen.

2. [Ausreisser und Noise](tasks/02_outliers_and_noise/README.md)  
   Von univariaten Regeln zu multivariaten Anomalien und fachlich begründeten Entscheidungen.

3. [Rückschätzung und Prognose](tasks/03_forecasting/README.md)  
   Von einem zweckspezifischen Analysedatensatz zu Backcast, Forecast und Managementaussage.

Die Aufgaben bauen aufeinander auf. Nach den ersten beiden Walkthroughs wird jeweils ein gemeinsamer Checkpoint bereitgestellt, damit alle Gruppen mit einer vergleichbaren Ausgangslage weiterarbeiten können.

## Daten und erwartete Struktur

Der Ausgangsdatensatz liegt unter:

```text
data/input/trips_case_initial.parquet
```

Eine Feldbeschreibung befindet sich in `data/README.md`. Diese Beschreibung legt fest, welche Spalten, Datentypen und Bedeutungen erwartet werden. In professionellen Datenplattformen wird eine solche Vereinbarung häufig als **Data Contract** bezeichnet.

Wichtig: Aggregationen sind zunächst nur diagnostische Sichten. Eine frühe stündliche Aggregation kann Auffälligkeiten sichtbar machen, entfernt aber die Evidenz auf Zeilenebene. Der endgültige stündliche Analysedatensatz entsteht deshalb erst, nachdem Replay-, Dubletten- und Qualitätsentscheidungen dokumentiert wurden.

## Einführung in Lektion 3

Die Kursleitung demonstriert denselben Fall aus zwei Perspektiven:

- **OpenRefine:** visuelles Profiling eines kleinen CSV-Ausschnitts mit Facetten, Missingness und auffälligen Kategorien;
- **Jupyter Notebook:** reproduzierbares Laden des Parquet-Bestands, programmatische Checks und erste Visualisierungen.

OpenRefine eignet sich hier für einen schnellen visuellen Einstieg. Der vollständige, wiederholbare Analysepfad wird anschliessend in Python weitergeführt. Die Demonstration soll bewusst zeigen, dass ein Werkzeug eine Beobachtung erleichtern kann, aber weder die fachliche Bedeutung noch die richtige Löschregel automatisch bestimmt.

## Einsatz von KI

KI ist Bestandteil jeder Aufgabe, aber nicht die Entscheidungsinstanz. Wir verwenden insbesondere ChatGPT und Claude Code in VS Code beziehungsweise Codespaces. Dabei gelten vier Regeln:

- Gebt Kontext, Ziel, Spaltenbedeutungen und Randbedingungen explizit an.
- Lasst euch Annahmen und Unsicherheiten ausgeben.
- Prüft erzeugten Code an kleinen, nachvollziehbaren Beispielen.
- Kontrolliert Änderungen als Diff und übernehmt sie nicht blind.

Im Tagesverlauf vergleichen wir hilfreiche und problematische Prompts. Dazu gehören vorschnelles Löschen von Ausreissern, erfundene Kausalgeschichten, unpassende Kennzahlen sowie Code, der zwar läuft, aber die fachliche Frage verändert.

## Datenschutz und verantwortungsvolle Nutzung

Der Workshop verwendet öffentliche und für den Unterricht aufbereitete Daten. Ladet dennoch keine vertraulichen, personenbezogenen oder unternehmensinternen Daten in externe KI-Dienste. In der Praxis müssen Datenschutz, Nutzungsbedingungen, Datenresidenz und interne Freigaben vor dem Einsatz geprüft werden.

## Gemeinsames Ziel

Am Ende soll keine vermeintlich «perfekt bereinigte» Universaltabelle stehen. Das Ziel sind nachvollziehbare, **zweckspezifische Datenprodukte**: beispielsweise eine Sicht für Nachfrage, eine andere für Umsatz und eine Quarantäne für noch ungeklärte Fälle. Jede wesentliche Transformation soll reproduzierbar und fachlich begründet sein.
