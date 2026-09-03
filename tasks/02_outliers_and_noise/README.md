[Workshop-Übersicht](../../README.md) · [Technische Vorbereitung](../../README_technical_preparation.md) · [Aufgabe 1: Datenqualität und Dubletten](../01_data_quality_and_duplicates/README.md) · [Aufgabe 2: Ausreisser und Noise](../02_outliers_and_noise/README.md) · [Aufgabe 3: Rückschätzung und Prognose](../03_forecasting/README.md)

---

# Aufgabe 2: Ausreisser, Anomalien und Noise

[Zur Workshop-Übersicht](../../workshop/README.md)

Diese Aufgabe wird in Lektion 7 bearbeitet. Ihr startet mit dem gemeinsam aufgelösten Ereignisbestand aus Aufgabe 1 und entscheidet, welche ungewöhnlichen Beobachtungen valide Extremfälle, klare Fehler oder noch ungeklärte Fälle sind.

## Ausgangslage

Das Management möchte ungewöhnlich lange und teure Fahrten aus der operativen Analyse entfernen. Ein Teammitglied schlägt vor, pauschal alle Werte ausserhalb der IQR-Grenzen und alle vom Isolation Forest markierten Zeilen zu löschen.

Eure Aufgabe ist es, diese Empfehlung zu prüfen. Ein Modell liefert Kandidaten, aber noch keine fachliche Wahrheit.

## Dateien

Gemeinsamer Ausgangspunkt nach dem ersten Walkthrough:

```text
data/checkpoints/checkpoint_01_resolved_events.parquet
```

Arbeitsnotebook:

```text
tasks/02_outliers_and_noise/task.ipynb
```

Zonenreferenz:

```text
data/reference/taxi_zone_lookup.csv
```

Die offizielle TLC-Tabelle ordnet `PULocationID` und `DOLocationID` einem Borough, Zonennamen und einer Service-Zone zu. Dokumentiert, welche externe oder fachliche Evidenz ihr tatsächlich verwendet.

## Lernziele

Nach der Aufgabe könnt ihr:

- univariate Ausreisserregeln als Screening einsetzen;
- Verteilungen mit robusten Kennzahlen und Visualisierungen beschreiben;
- multivariate Anomalien mit geeigneten Features untersuchen;
- Modellscore, fachliche Plausibilität und Datenfehler unterscheiden;
- Fälle den Aktionen **behalten**, **ausschliessen** oder **prüfen** zuordnen;
- die Auswirkung einer Qualitätsregel auf verschiedene Datenprodukte erklären.

## Teil A: Verteilungen und abgeleitete Merkmale

Erzeugt nachvollziehbare Merkmale, mindestens:

- Fahrtdauer in Minuten;
- mittlere Geschwindigkeit aus Distanz und Dauer;
- Betrag pro Meile oder eine vergleichbare Verhältnisgrösse;
- Stunde und Wochentag des Ereignisses.

Prüft vor jeder Division ungültige oder nichtpositive Nenner. Beschreibt anschliessend die Verteilungen von Distanz, Dauer, Geschwindigkeit und Betrag mit Quantilen, Histogrammen und geeigneten Boxplots.

Fragen:

- Sind die Verteilungen symmetrisch oder stark rechtsschief?
- Welche Transformation oder logarithmische Darstellung erleichtert die Exploration?
- Welche extremen Werte sind bereits durch einfache Plausibilitätsbedingungen auffällig?
- Welche Extremwerte könnten für Flughäfen, Fernfahrten oder Sondertarife plausibel sein?

## Teil B: IQR als Kandidatengenerator

Berechnet für mindestens eine zentrale Variable die IQR-Grenzen:

\[
IQR = Q_{0.75} - Q_{0.25}
\]

\[
\text{untere Grenze} = Q_{0.25} - 1.5 \cdot IQR, \qquad
\text{obere Grenze} = Q_{0.75} + 1.5 \cdot IQR
\]

Kennzeichnet die Treffer als `iqr_candidate`, nicht als automatisch fehlerhaft.

Untersucht Stichproben knapp oberhalb der Grenze und aus dem äussersten Rand. Prüft, ob dieselbe globale Grenze für alle Tarifarten, Zonen und Tageszeiten sinnvoll ist.

## Teil C: Multivariate Anomalien

Trainiert einen Isolation Forest oder verwendet das bereitgestellte Gerüst. Wählt nur Features, deren Bedeutung ihr erklären könnt. Behandelt kategoriale Codes nicht unbesehen als kontinuierliche Messwerte.

Dokumentiert:

- verwendete Features und Vorverarbeitung;
- Behandlung fehlender und unendlicher Werte;
- gewählten Anteil erwarteter Anomalien beziehungsweise Modellparameter;
- Zufallsstart für Reproduzierbarkeit;
- Unterschied zwischen Modellscore und finaler Entscheidung.

Vergleicht die Modellkandidaten mit der IQR-Regel:

- Welche Fälle markieren beide Methoden?
- Welche Fälle findet nur eine Methode?
- Welche fachlich plausiblen Extremfälle würden bei blindem Löschen verloren gehen?
- Welche Kombinationen, etwa sehr kurze Dauer und sehr grosse Distanz, deuten klarer auf Noise hin?

## Teil D: Evidenz und Entscheidung

Bildet für verdächtige Fälle eine kompakte Prüftabelle. Ergänzt mindestens:

- ursprüngliche Messwerte;
- abgeleitete Dauer und Geschwindigkeit;
- Tarif- und Zoneninformationen;
- Treffer der IQR- und Modellregeln;
- fachliche Begründung;
- Aktion: `keep`, `exclude` oder `review`;
- betroffene Zielsicht.

Nutzt Lookup-Daten oder dokumentierte externe Recherche, um einzelne Extremfälle zu plausibilisieren. Eine ungewöhnliche Zielzone oder ein Sondertarif kann eine lange Fahrt erklären; eine physikalisch unmögliche Kombination hingegen nicht.

Beantwortet:

1. Welche Regeln liefern nur Untersuchungsfälle?
2. Welche Kombinationen erlauben eine klare Noise-Kennzeichnung?
3. Welche Fälle sind valide Extremwerte und müssen erhalten bleiben?
4. Welche Fälle bleiben mehrdeutig und gehören in Quarantäne?
5. Unterscheiden sich die Entscheidungen für Nachfrage, Umsatz und Fahrtdauer?

## KI-Experiment: Kontext und Werkzeugwahl

Gebt ChatGPT eine kleine, anonymisierte Prüftabelle und bittet um eine Klassifikation. Vergleicht zwei Varianten:

- nur die numerischen Werte;
- dieselben Werte plus Spaltenbeschreibung, Tarif- und Zoneninformation sowie erlaubte Aktionen.

Prüft, ob die KI fachliche Regeln erfindet oder aus einem Anomaliescore direkt «Fehler» ableitet.

Optional demonstriert die Kursleitung dieselbe Analyse in einer Online-Toolbox mit wenig Projektkontext. Achtet darauf, ob dabei Umgebungsabhängigkeiten, Dateipfade, Reproduzierbarkeit oder fachliche Definitionen verloren gehen. Die Plattform ist nicht pauschal «schlecht»; der Negativfall entsteht durch einen ungeeigneten Workflow.

## Erwartetes Ergebnis der Gruppe

Am Ende präsentiert jede Gruppe:

- eine Visualisierung der wichtigsten Verteilungen;
- Vergleich von IQR- und multivariaten Kandidaten;
- je mindestens einen validen Extremfall, klaren Noise-Fall und Review-Fall;
- eine begründete Entscheidungslogik statt einer reinen Modellschwelle;
- erwartete Auswirkungen auf mindestens zwei Zielsichten;
- eine beobachtete Stärke und eine Schwäche der KI-Unterstützung.

## Nach dem Walkthrough

Nach der Besprechung werden Musterlösung und gemeinsamer Qualitätscheckpoint unter neuen Dateinamen veröffentlicht. Eure Datei `task.ipynb` wird nicht überschrieben. Aufgabe 3 beginnt mit:

```text
data/checkpoints/checkpoint_02_reviewed_quality.parquet
```

Die Erläuterung wird nach der Gruppenphase unter `tasks/02_outliers_and_noise/released/WALKTHROUGH.md` freigeschaltet.
