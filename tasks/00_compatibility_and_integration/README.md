[Workshop-Übersicht](../../README.md) · [Technische Vorbereitung](../../README_technical_preparation.md) · [Aufgabe 0: Kompatibilität und Integration](../00_compatibility_and_integration/README.md) · [Aufgabe 1: Datenqualität und Dubletten](../01_data_quality_and_duplicates/README.md) · [Aufgabe 2: Ausreisser und Noise](../02_outliers_and_noise/README.md) · [Aufgabe 3: Rückschätzung und Prognose](../03_forecasting/README.md)

---

# Aufgabe 0 · Kompatibilität und Integration

Um 10:45 Uhr fragt die Schichtleiterin nach der letzten Wartung von Maschine M1. Im Log steht eine Kalibrierung um 11:00 Uhr. Welche Wartung darf auf dem Dashboard um 10:45 Uhr erscheinen? Und welche Messwerte dürft ihr später für eine Temperaturprognose verwenden?

Öffnet das [Arbeitsnotebook](task.ipynb). Arbeitet zu zweit oder zu dritt und dokumentiert eure Entscheide direkt bei den Ergebnissen. Für diesen Einstieg benötigt ihr vier CSV-Dateien aus Übung 9.

## Datengrundlage

| Datei | Was beschreibt eine Zeile? | Felder für die Zuordnung |
| --- | --- | --- |
| [zeitreihe_roh.csv](data/zeitreihe_roh.csv) | Messzeitpunkt mit Temperatur und Vibration, teilweise mit fehlenden Werten | `machine_id`, `timestamp` |
| [maschinenstamm.csv](data/maschinenstamm.csv) | Maschine mit Standort, Inbetriebnahmedatum und Kritikalität | `machine_id` |
| [wartung.csv](data/wartung.csv) | Beginn einer Wartung mit Typ und zuständiger Person | `machine_id`, `maintenance_start` |
| [prognose_zielreihe.csv](data/prognose_zielreihe.csv) | Referenztemperatur für einen Teil des Messzeitraums | `machine_id`, `timestamp` |

## Arbeitsauftrag

| Teil | Auftrag | Woran erkennt ihr ein plausibles Ergebnis? |
| --- | --- | --- |
| **A · Kompatibilität prüfen** | Untersucht Datentypen, Schlüssel, Bedeutung, Messraster und zeitliche Abdeckung. Prüft, ob die Zeitangaben eine Zeitzone und die Signale eine Einheit ausweisen. | Ihr könnt erklären, wo ein exakter Schlüssel genügt und wo dieselbe Maschinen-ID mehrere Ereignisse bezeichnet. |
| **B · Lücken behandeln** | Vergleicht Forward Fill, Backward Fill und zeitbasierte lineare Interpolation separat für Temperatur und Vibration. Behaltet die Rohwerte und kennzeichnet imputierte Werte. | Für die Temperaturlücke um 08:45 Uhr könnt ihr zwischen einer Live-Schätzung und einer nachträglichen Rekonstruktion entscheiden. |
| **C · Daten integrieren** | Ergänzt die Messungen um Standort, Kritikalität und die zuletzt begonnene Wartung derselben Maschine. Prüft die Anzahl und Eindeutigkeit der Messungen nach jedem Join. | Zeigt die Zuordnung unmittelbar vor und genau beim Wartungsbeginn um 11:00 Uhr. |
| **D · Temperatur schätzen** | Glättet die historische Temperatur mit einem gleitenden Mittel. Vergleicht sie im überlappenden Zeitraum mit der Referenzreihe. Testet anschliessend zwei einfache Prognosen ab 11:45 Uhr und extrapoliert ab 17:45 Uhr nochmals vier Viertelstunden. | Zeigt den mittleren absoluten Fehler (MAE) in °C dort, wo Referenzwerte vorliegen. Begründet die Unsicherheit der letzten vier Prognosen. |

**Für die Besprechung:** Bringt eure integrierte Tabelle, den Vergleich von Schätzung und Referenz sowie die vier Prognosewerte je Methode mit. Haltet im Decision Log fest, welche Join-Regel und welche Art der Imputation ihr im laufenden Betrieb einsetzen würdet.

[Walkthrough](WALKTHROUGH.md) · [Musterlösung](task_sample_solution.ipynb) · [Weiter zu Aufgabe 1](../01_data_quality_and_duplicates/README.md)
