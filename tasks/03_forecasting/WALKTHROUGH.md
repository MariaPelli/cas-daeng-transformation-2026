# Walkthrough 3: Rückschätzung, Prognose und Managementaussage

> **Kursleitungsintern bis zum Walkthrough in Lektion 9.** Danach zusammen mit den Istwerten und der Musterlösung unter `tasks/03_forecasting/released/` veröffentlichen.

[Zur Aufgabenstellung](../README.md) · [Zur Workshop-Übersicht](../../../workshop/README.md)

## Ziel des Walkthroughs

Der Abschluss verbindet Datenqualität und Prognose. Nicht ein komplexes Modell, sondern ein kontrollierter Vergleich soll zeigen:

- welche Zielsicht prognostiziert wird;
- wie Leakage verhindert wird;
- ob Bereinigung die Prognose messbar verändert;
- wie Resultate ohne erfundene Kausalität kommuniziert werden.

## 1. Vier Datenprodukte statt einer Clean Table

Die Referenzpipeline erzeugt aus denselben angereicherten Rohzeilen vier Sichten:

| Datenprodukt | Zeilen | Zweck |
|---|---:|---|
| `trips_for_demand` | 195'756 | physische Fahrten für Nachfrage |
| `events_for_revenue` | 199'958 | finanzielle Ereignisse für Nettoumsatz |
| `trips_for_duration` | 186'135 | plausible Fahrten für Dauer- und Geschwindigkeitsanalysen |
| `quarantined_records` | 13'942 | Audit- und Review-Bestand |

Zum Vergleich enthält das Rohsample 200'900 Zeilen.

### Entscheidungslogik

- Technische Replays und Payload-Kopien zählen in keiner produktiven Sicht erneut.
- Die 41 klaren Noise-Fälle werden ausgeschlossen.
- Negative Finanzereignisse zählen nicht als zusätzliche physische Fahrt.
- Positive und negative Finanzereignisse bleiben in `events_for_revenue`, sofern sie keine technischen Kopien oder klarer Noise sind.
- Für `trips_for_duration` gelten zusätzlich positive Dauer, positive Distanz, maximal 12 Stunden Dauer und eine Geschwindigkeit zwischen 0.1 und 120 mph.

`quarantined_records` ist eine Audit-Sicht und nicht zwingend disjunkt zu allen fachlichen Sichten. Ein Review-Fall kann zum Beispiel für Demand enthalten, aber für Duration ausgeschlossen sein.

### Kontrollwerte

| Kennzahl | Rohsample | zweckspezifische Sicht |
|---|---:|---:|
| Umsatzsumme | 5'410'768.61 | 5'383'370.81 in `events_for_revenue` |
| Median Fahrtdauer | 13.52 min | 13.72 min in `trips_for_duration` |

Die Umsatzdifferenz entsteht nicht durch das Entfernen aller negativen Beträge. Gegenbuchungen bleiben für die Nettosicht relevant; entfernt werden technische Wiederholungen und klare Fehler.

## 2. Vollständige stündliche Zeitreihe

```python
def hourly_counts(df, start, end):
    index = pd.date_range(
        start,
        pd.Timestamp(end) - pd.Timedelta(hours=1),
        freq="h",
    )
    counts = df.groupby(
        df["tpep_pickup_datetime"].dt.floor("h")
    ).size()
    return counts.reindex(index, fill_value=0).astype(float)
```

Für Training und Backcast wird das Intervall `[2025-07-01, 2025-07-25)` verwendet. Dadurch entstehen 24 vollständige Tage. Roh- und Demand-Sicht müssen exakt denselben Stundenindex verwenden.

Die Aggregation erfolgt erst nach den Ereignis- und Qualitätsentscheidungen. Sonst könnte ein Replay-Peak auf Stundenebene erkannt, aber nicht mehr einzelnen Batch- oder Payload-Zeilen zugeordnet werden.

## 3. Rückschätzung des 10. Juli

Der 10. Juli 2025 wird vollständig maskiert. Seine 24 Iststunden werden erst nach der Modellbildung zur Evaluation verwendet.

Verglichene Verfahren:

1. Zeitinterpolation über die 24-Stunden-Lücke;
2. Median derselben Stunde an anderen Donnerstagen;
3. lineares Kalendermodell mit Stunde, Wochentag und Trend.

Ergebnisse der bereinigten Demand-Sicht:

| Verfahren | MAE | WAPE |
|---|---:|---:|
| Interpolation | 195.1400 | 0.5442 |
| Wochentag/Stunde-Median | 27.2917 | 0.0761 |
| lineares Kalendermodell | 84.0035 | 0.2343 |

### Interpretation

Interpolation verbindet lediglich die Stunden vor und nach einer ganzen Tageslücke. Sie bildet das Tagesprofil nicht ab und ist deshalb klar ungeeignet. Der Wochentag/Stunde-Median nutzt die starke wiederkehrende Saisonalität und ist hier die beste, zugleich einfachste Methode.

Bei einem zusätzlichen Roh-versus-bereinigt-Vergleich müssen beide Serien mit identischem Maskenfenster und identischen Verfahren berechnet werden. Der wichtigste Reveal dieser Rückschätzung ist die Methodenannahme, nicht ein künstlich erzwungener grosser Cleaning-Effekt: Der kontrollierte Replay liegt nicht am 10. Juli.

### Leakage-Prüfung

- Der maskierte Tag darf nicht in Median-Lookups oder Modelltraining enthalten sein.
- Features dürfen nur aus Zeitstempeln und verfügbarem Training stammen.
- Die Istwerte werden erst in `error_metrics()` mit den Prognosen verbunden.

## 4. Zukunftsprognose vom 25. bis 31. Juli

Der verdeckte Holdout umfasst **168 Stunden**. Die erste Baseline ist saisonal-naiv:

```python
def seasonal_naive(training, target_index):
    lookup = target_index - pd.Timedelta(hours=168)
    return pd.Series(
        training.reindex(lookup).to_numpy(),
        index=target_index,
    )
```

Der kontrollierte Replay betrifft Freitag, 18. Juli, 17:00–21:00 Uhr. Eine 168-Stunden-Baseline aus der Rohsicht kopiert diesen technischen Peak genau auf Freitag, 25. Juli. Die bereinigte Demand-Sicht verhindert diese Fortschreibung.

### Resultate nach Offenlegung des Holdouts

| Modell und Trainingssicht | MAE | WAPE |
|---|---:|---:|
| saisonal-naiv, Rohsicht | 45.0833 | 0.1214 |
| saisonal-naiv, Demand-Sicht | 42.2083 | 0.1136 |
| lineares Kalendermodell, Rohsicht | 86.0583 | 0.2317 |
| lineares Kalendermodell, Demand-Sicht | 83.0854 | 0.2237 |

Die Bereinigung verbessert beide Modellvarianten. Das saisonal-naive Modell bleibt deutlich besser als das lineare Kalendermodell. Mehr Komplexität ist hier also weder automatisch genauer noch fachlich leichter zu rechtfertigen.

Für die saisonale Baseline sinkt der MAE um 2.875 Fahrten pro Stunde und der WAPE um rund 0.77 Prozentpunkte. Dieser Unterschied ist klein genug für eine nüchterne Interpretation und gross genug, um den gezielt fortgeschriebenen Replay-Effekt sichtbar zu machen.

## 5. Beispiel einer Managementaussage

> Im Rohbestand wurden wiederholt eingelesene Fahrtereignisse und einzelne physikalisch nicht plausible Datensätze gefunden. Für die Nachfrageprognose haben wir technische Replays, Gegenbuchungen als zusätzliche Fahrten und klaren Noise ausgeschlossen, ohne plausible Fernfahrten pauschal zu entfernen. Im verdeckten Zeitraum erreichte die saisonal-naive Prognose auf der bereinigten Nachfragesicht einen WAPE von 11.36 % gegenüber 12.14 % auf der Rohsicht. Sie schnitt zugleich deutlich besser ab als das getestete lineare Kalendermodell. Wir empfehlen die bereinigte saisonale Baseline als transparenten Ausgangspunkt, verbunden mit laufendem Monitoring der Replay- und Quarantäneregeln. Die Auswertung zeigt einen belastbaren Zusammenhang mit der Datenbereinigung, ersetzt aber keine technische Root-Cause-Analyse des Ingest-Vorfalls.

Die Aussage benennt Datenprodukt, Vergleich, Kennzahl, Empfehlung und Grenze. Sie behauptet nicht, dass jeder Peak durch denselben technischen Fehler verursacht wurde.

## 6. Modularisierung aus Lektion 8

Die Musterlösung sollte mindestens folgende kleine Funktionen enthalten:

```text
add_features(df)
add_quality_flags(df, expected_start, expected_end)
build_views(df, expected_start, expected_end)
hourly_counts(df, start, end)
seasonal_naive(training, target_index)
calendar_features(index, origin)
error_metrics(actual, predicted)
```

Zu prüfen sind insbesondere:

- Funktionen verändern den Input nicht unbeabsichtigt;
- Zeitintervalle sind als `[start, end)` dokumentiert;
- der Stundenindex ist vollständig;
- `random_state` ist gesetzt, wo Zufall verwendet wird;
- Views werden aus Flags gebaut und nicht durch verstreute Löschbefehle;
- Kontrollwerte und Grenzfälle sind als Tests formulierbar.

## 7. KI-Retrospektive

Die Texte von ChatGPT und Claude Code können variieren. Bewertet deshalb nicht nach Stil, sondern anhand derselben Checkliste:

| Prüfkriterium | Erwartung |
|---|---|
| Zahlen | stimmen mit der Evaluation überein |
| Kausalität | kein unbelegter Ursachenbeweis |
| Unsicherheit | relevante Einschränkung wird genannt |
| Modellauswahl | folgt transparenter Kennzahl und Einsatzzweck |
| Codeänderung | bleibt im beauftragten Umfang und ist als Diff prüfbar |
| Reproduzierbarkeit | Pfade, Parameter und Tests bleiben dokumentiert |

Typische Fehlleistungen:

- WAPE wird als «Genauigkeit» statt als relativer absoluter Fehler beschrieben;
- Prozent und Prozentpunkte werden verwechselt;
- aus einer Verbesserung wird eine garantierte zukünftige Wirkung abgeleitet;
- das komplexere Modell wird trotz schlechterer Werte empfohlen;
- Claude Code verändert nebenbei Datenpfade oder andere Dateien;
- eine elegante Zusammenfassung verschweigt die zweckspezifische Definition der Nachfragesicht.

### Best Practices für den Abschluss

1. Erst fachliches Ziel und Datensicht definieren, dann KI beauftragen.
2. Beide Systeme mit identischem, minimal ausreichendem Kontext vergleichen.
3. Zahlen automatisiert aus Ergebnistabellen übernehmen und gegenprüfen.
4. Änderungen in kleinen Schritten und als Diff kontrollieren.
5. Modellannahmen und verbleibende Unsicherheit explizit verlangen.
6. KI-Ausgaben als Entwurf behandeln; Verantwortung bleibt beim Menschen.

## Kernaussage für den Tagesabschluss

Die Qualität einer Prognose beginnt vor dem Modell. Reproduzierbare Ereignislogik, zweckspezifische Views und ein ehrliches Backtesting sind wertvoller als ein komplexeres Verfahren auf einem unklar definierten Datensatz.
