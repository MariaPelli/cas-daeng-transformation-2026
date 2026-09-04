# Walkthrough 2: Ausreisser, Anomalien und Noise

> **Kursleitungsintern bis zum Ende von Lektion 7.** Erst nach der Gruppenarbeit unter `tasks/02_outliers_and_noise/released/WALKTHROUGH.md` veröffentlichen.

[Zur Aufgabenstellung](../README.md) · [Zur Workshop-Übersicht](../../../workshop/README.md)

## Ziel des Walkthroughs

Die Auflösung soll drei Kategorien sichtbar machen:

1. statistisch ungewöhnlich, aber fachlich plausibel;
2. durch mehrere Evidenzen klar als Noise begründbar;
3. auffällig, aber ohne ausreichende Evidenz für eine endgültige Klassifikation.

IQR und Isolation Forest priorisieren die Untersuchung. Sie liefern keine Wahrheitslabels.

## 1. Transparente Merkmale

```python
import numpy as np

df["duration_min"] = (
    df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
).dt.total_seconds() / 60

df["speed_mph"] = np.where(
    df["duration_min"] > 0,
    df["trip_distance"] / (df["duration_min"] / 60),
    np.nan,
)

df["amount_per_mile"] = np.where(
    df["trip_distance"] > 0,
    df["total_amount"] / df["trip_distance"],
    np.nan,
)
```

Vor der Modellierung werden `NaN`, positive und negative Unendlichkeit explizit behandelt. Dauer und Geschwindigkeit bleiben als interpretierbare Prüfgrössen erhalten.

## 2. IQR: viele Kandidaten, wenig Gewissheit

Für `trip_distance` ergibt die Tukey-Regel:

| Kennzahl | Ergebnis |
|---|---:|
| obere IQR-Grenze | 8.22 Meilen |
| Beobachtungen oberhalb der Grenze | 23'289 |

Die Trefferzahl ist absichtlich gross. New Yorker Taxifahrten haben eine rechtsschiefe Distanzverteilung; mehr als 8.22 Meilen ist ungewöhnlich, aber keineswegs automatisch falsch.

### Didaktischer Vergleich

Zeigt zwei Gruppen nebeneinander:

- extreme Distanzen von mehreren hunderttausend Meilen bei Fahrtdauern unter einer halben Stunde;
- Fahrten von mehreren hundert Meilen mit mehreren Stunden Dauer, Sondertarif und plausibler Geschwindigkeit.

Beide liegen weit ausserhalb der IQR-Grenze. Nur die erste Gruppe verletzt zugleich physische Plausibilität.

## 3. Isolation Forest: anderer Kandidatengenerator

Die Referenz verwendet für Zeilen mit positiver Dauer:

```python
X = pd.DataFrame({
    "log_distance": np.log1p(model_frame["trip_distance"].clip(lower=0)),
    "log_duration": np.log1p(model_frame["duration_min"].clip(lower=0)),
    "log_abs_total": np.log1p(model_frame["total_amount"].abs()),
}).replace([np.inf, -np.inf], np.nan).fillna(0)

model = IsolationForest(
    n_estimators=100,
    contamination=0.01,
    random_state=20250902,
    n_jobs=-1,
)
```

Ergebnis: **1'980 Isolation-Forest-Kandidaten**.

Die Anzahl folgt teilweise aus `contamination=0.01`. Sie ist keine empirisch bewiesene Fehlerquote. Ein anderer Parameter oder eine andere Featureauswahl verändert die Markierungen.

## 4. Fachliche Evidenz

### Klare Noise-Fälle

Die Referenzregel für unmögliche Geschwindigkeit lautet:

```python
is_impossible_speed = (
    (df["trip_distance"] >= 10)
    & (df["duration_min"] > 0)
    & (df["speed_mph"] > 300)
)
```

Sie markiert **38 Fälle**. Zusätzlich liegen **3 Pickup-Zeitstempel** klar ausserhalb des erwarteten Zeitfensters. Zusammen ergeben diese Regeln **41 klare Noise-Fälle** für die Nachfragesicht.

Die Schwellen sind bewusst konservativ. Sie sollen nur Fälle automatisch ausschliessen, bei denen mehrere Merkmale gemeinsam eine physikalisch beziehungsweise zeitlich nicht plausible Beobachtung bilden.

### Valide Extremfälle

Die Instructor-Labels enthalten **32 valide Fernfahrten**. Typische Evidenz:

- Distanz zwischen ungefähr 60 und 500 Meilen;
- Dauer zwischen 30 und 600 Minuten;
- plausible mittlere Geschwindigkeit;
- Sondertarif, insbesondere `RatecodeID` 3, 4 oder 5;
- häufig `DOLocationID = 265`, also eine Zone ausserhalb der regulären kartierten Taxizonen.

Diese Fahrten bleiben erhalten. Das Ground-Truth-Audit bestätigt, dass alle 32 in der späteren Duration-Sicht enthalten sind.

### Monatsgrenze

Neben den drei ungültigen Zeitstempeln existieren **4 legitime Grenzübertritte**: Pickup kurz vor Beginn des Monats, Dropoff nach Monatsbeginn. Eine blosse Regel `pickup < 2025-07-01` würde diese fälschlich entfernen. Der Zeitkontext beider Spalten ist entscheidend.

### Mehrdeutige Qualitätsfälle

| Hinweis | Zeilen | Behandlung in der Referenz |
|---|---:|---|
| Distanz gleich null | 6'176 | Review; für Daueranalyse ausschliessen |
| Dauer kleiner oder gleich null | 2'984 | Review; für Daueranalyse ausschliessen |
| Geschwindigkeit über 120 mph | 77 | Review; nur strengere Kombinationen automatisch ausschliessen |

Diese Kategorien können sich überlappen. Eine Zeile in der Quarantäne- oder Review-Tabelle muss nicht aus jeder Zielsicht verschwinden. Beispielsweise kann eine Null-Distanz-Fahrt für eine Nachfragezählung noch als Ereignis zählen, obwohl sie für eine Geschwindigkeits- oder Daueranalyse ungeeignet ist.

## 5. Entscheidungsraster

| Evidenz | Klasse | Demand | Revenue | Duration |
|---|---|---|---|---|
| nur IQR-Treffer | Kandidat | vorläufig behalten | vorläufig behalten | prüfen |
| nur Isolation-Forest-Treffer | Kandidat | vorläufig behalten | vorläufig behalten | prüfen |
| plausible Dauer, Geschwindigkeit und Sondertarif | valider Extremfall | behalten | behalten | behalten |
| extreme Distanz plus über 300 mph | klarer Noise | ausschliessen | ausschliessen | ausschliessen |
| ungültiger Zeitstempel ausserhalb des erwarteten Fensters | klarer Noise | ausschliessen | ausschliessen | ausschliessen |
| Null-Distanz oder nichtpositive Dauer ohne weitere Evidenz | Review | je nach Ziel behalten | je nach Ziel behalten | ausschliessen |

Die Umsatzsicht schliesst klare technische beziehungsweise physische Fehler aus, behält aber legitime negative Finanzereignisse aus Aufgabe 1.

## 6. Warum globale Löschregeln scheitern

- `trip_distance > 8.22` würde zehntausende plausible längere Fahrten entfernen.
- «Isolation Forest = Fehler» verwechselt ein Ranking mit Ground Truth.
- Eine globale Geschwindigkeitsgrenze ohne Dauerprüfung erzeugt Divisionseffekte.
- Eine Zeitfensterprüfung nur auf Pickup übersieht legitime Grenzübertritte.
- Ein einziges Clean-Flag verschleiert, dass eine Zeile für Demand brauchbar und für Duration ungeeignet sein kann.

## 7. Übergabe-Checkpoint

`data/checkpoints/checkpoint_02_reviewed_quality.parquet` soll weiterhin alle Rohzeilen und Lineage-Felder enthalten, ergänzt um mindestens:

- `duration_min`;
- `speed_mph`;
- `iqr_candidate`;
- `isolation_candidate` oder den Modellscore;
- `is_invalid_timestamp`;
- `is_boundary_crossing`;
- `is_impossible_speed`;
- `is_clear_noise`;
- einen oder mehrere Review-Gründe;
- eine dokumentierte Aktion je Zielsicht oder die dafür nötigen Flags.

Die Gruppenergebnisse müssen nicht dieselbe Zahl an Modellkandidaten liefern, wenn Features oder Parameter begründet anders gewählt wurden. Die 41 klaren Noise-Fälle und 32 validen Fernfahrten dienen im Referenzlauf als kontrollierbare Anker.

## 8. KI-Retrospektive

Mit rein numerischen Werten neigt ein Sprachmodell dazu, plausible Domänengeschichten zu erfinden. Mit Tarif-, Zonen- und Feldbeschreibung kann es bessere Prüffragen vorschlagen, besitzt aber weiterhin keinen Beweis für die reale Fahrt.

Besonders kritisch sind:

- erfundene Bedeutungen von Codes;
- unbelegte Aussagen wie «Betrug» oder «Sensorfehler»;
- eine Klassifikation ohne Unsicherheitskategorie;
- Code, der Modellkandidaten direkt löscht;
- eine Online-Analyse, die Dateiversion, Environment oder Parameter nicht dokumentiert.

Der passende Output einer KI ist hier eine **prüfbare Hypothese oder Codehilfe**, nicht die endgültige fachliche Entscheidung.

## Kernaussage für den Abschluss

Ausreissererkennung ist Triage. Noise wird erst durch die Kombination aus statistischem Signal, physischer Plausibilität, Domänenwissen und dokumentiertem Analysezweck begründet.
