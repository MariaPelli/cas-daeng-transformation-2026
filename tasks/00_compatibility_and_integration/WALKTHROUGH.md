# Walkthrough 0 · Kompatibilität und Integration

[Aufgabenstellung](README.md) · [Ausführbare Musterlösung](task_sample_solution.ipynb) · [Workshop-Übersicht](../../README.md)

## A · Vier Dateien, vier Bedeutungen

Lasst die Gruppen zunächst erklären, wie viele Messungen sie nach der Integration erwarten. Die **40 Messzeitpunkte von M1** bilden die Ausgangsmenge. Sie liegen am 1. Januar 2025 von 08:00 bis 17:45 Uhr im 15-Minuten-Raster. Bei sieben Messungen fehlt die Temperatur, bei drei die Vibration. Das Raster selbst ist vollständig. Der Stamm umfasst M1 und M2. Das Wartungslog enthält zwei Ereignisse für M1 und eines für M2. Die 20 Referenzwerte für M1 reichen von 08:00 bis 12:45 Uhr.

| Prüfung | Befund | Konsequenz |
| --- | --- | --- |
| Format | Maschinenkennungen sind Text. Zeitangaben lassen sich als Datum bzw. Zeitstempel lesen. | Die Zeitspalten vor Sortierung, Zeitvergleich und Join explizit parsen. |
| Bedeutung | Eine Messung, ein Wartungsbeginn und eine Referenztemperatur bezeichnen unterschiedliche Sachverhalte. | Die Temperaturreferenz dient der Bewertung. Anfang und Ende einer Wartung wären getrennte Merkmale. |
| Granularität | Der Stamm hat eine Zeile je Maschine, Messungen und Wartungen haben mehrere Zeitpunkte je Maschine. | Der Stamm-Join ist Viele-zu-eins. Beim Wartungs-Join ist zusätzlich eine Auswahlregel nötig. |
| Zeit und Einheiten | Die CSVs nennen keine Zeitzone. Die Vorlage behandelt die Temperatur als °C. Eine Vibrationseinheit fehlt. | Für diese Übung eine gemeinsame Uhrzeit und Temperaturskala annehmen. Vor einer betrieblichen Nutzung die Metadaten klären. |

## B · Die Lücke um 08:45 Uhr

Um 08:30 Uhr meldet M1 **21.09 °C**, der nächste gültige Wert folgt um 09:15 Uhr mit **21.76 °C**. Dazwischen fehlen zwei Temperaturwerte.

| Zeitpunkt | Forward Fill | Backward Fill | Zeitbasierte Interpolation |
| --- | ---: | ---: | ---: |
| 08:45 | 21.09 | 21.76 | 21.31 |
| 09:00 | 21.09 | 21.76 | 21.54 |

Bei der ersten Lücke ist ein Drittel der 45 Minuten verstrichen. Die Interpolation addiert daher ein Drittel der Differenz von 0.67 °C. Das ist rückblickend plausibel, sofern sich die Temperatur annähernd stetig verändert hat. Um 08:45 Uhr war nur der frühere Messwert verfügbar. Forward Fill gibt dann eine begründbare Live-Schätzung. Ein Flag hält fest, dass der Sensor zu diesem Zeitpunkt keinen Temperaturwert geliefert hat.

## C · Warum der zweite Join eine Zeitregel braucht

Ein Left Join mit dem eindeutigen Maschinenstamm erhält alle **40** Zeitpunkte und ergänzt für M1 **Halle_A** und die Kritikalität **hoch**. Ein anschliessender Join mit Wartungen allein auf `machine_id` liefert **80** Zeilen, weil jede der 40 Messungen beide Wartungen von M1 trifft.

Die Musterlösung sortiert beide Tabellen nach ihrer jeweiligen Zeitspalte. `merge_asof` sucht mit `by="machine_id"` und `direction="backward"` das jüngste Ereignis mit einem Beginn bis einschliesslich Messzeitpunkt. Das Ergebnis hat wieder genau eine Zeile je Messung.

| Messzeitpunkt M1 | Zugeordneter Beginn | Wartung |
| --- | --- | --- |
| 1. Januar, 10:45 | 15. Dezember 2024, 09:00 | Inspektion |
| 1. Januar, 11:00 | 1. Januar 2025, 11:00 | Kalibrierung |

**Frage für die Gruppe:** «War M1 um 11:15 Uhr noch in Kalibrierung?» Das Log liefert nur den Beginn. Für eine Aussage über die Dauer bräuchte man eine Endzeit. Ob ein Ereignis im operativen System sofort sichtbar war, liesse sich mit einem zusätzlichen Eingangszeitpunkt prüfen.

## D · Eine Referenzreihe für zwei verschiedene Fragen

**Wie gut beschreiben wir den beobachteten Verlauf?** Die Musterlösung interpoliert die Temperatur, bildet ein nachlaufendes Mittel über drei Messungen und nutzt am Reihenanfang die verfügbaren Werte. Beim exakten Join mit der Referenz auf Maschine und Zeitpunkt entstehen **20 Paare**. Der mittlere absolute Fehler (MAE) beträgt **1.068 °C**. Dieser Wert beschreibt die rückblickende Approximation.

**Was hätten wir um 11:45 Uhr für die nächste Stunde vorhergesagt?** Wir schneiden die Eingabe um 11:45 Uhr ab und verwenden die vorwärts gefüllte Temperatur. Das lokale Trendmodell passt eine Gerade an die letzten vier Viertelstunden an. Die Vergleichsmethode schreibt die letzte verfügbare Temperatur fort. Erst nach beiden Vorhersagen ziehen wir die vier Referenzwerte heran.

| Prognosezeit | Referenz (°C) | Letzter Wert (°C) | Linearer Trend (°C) |
| --- | ---: | ---: | ---: |
| 12:00 | 22.77 | 23.54 | 23.255 |
| 12:15 | 22.84 | 23.54 | 23.113 |
| 12:30 | 22.84 | 23.54 | 22.971 |
| 12:45 | 22.84 | 23.54 | 22.829 |
| **MAE (°C)** | | **0.7175** | **0.225** |

**Was lässt sich nach Schichtende sagen?** Mit den letzten vier Viertelstunden bis 17:45 Uhr ergeben sich folgende Prognosen.

| Prognosezeit | Letzter Wert (°C) | Linearer Trend (°C) |
| --- | ---: | ---: |
| 18:00 | 20.800 | 20.050 |
| 18:15 | 20.800 | 19.708 |
| 18:30 | 20.800 | 19.366 |
| 18:45 | 20.800 | 19.024 |

Der Trend lag im historischen Testfenster näher an der Referenz. Ein einziges Fenster mit vier Punkten reicht für eine allgemeine Modellwahl kaum aus. Für 18:00 bis 18:45 Uhr fehlen Vergleichswerte. Die Differenz zwischen den beiden Vorschauen zeigt, wie stark die Annahme über die Fortsetzung des letzten Trends die Aussage für die Schichtleitung verändert.

[Weiter zu Aufgabe 1 · Datenqualität und Dubletten](../01_data_quality_and_duplicates/README.md)
