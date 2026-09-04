# Walkthrough 1: Datenqualität, Duplikate und Dubletten

> **Kursleitungsintern bis zum Ende von Lektion 4.** Erst nach der Gruppenarbeit unter `tasks/01_data_quality_and_duplicates/released/WALKTHROUGH.md` veröffentlichen.

[Zur Aufgabenstellung](../README.md) · [Zur Workshop-Übersicht](../../../workshop/README.md)

## Ziel des Walkthroughs

Der Walkthrough soll nicht nur die «richtigen Zahlen» zeigen. Die zentrale Story lautet:

1. Ein auffälliger Peak kann ein reales Ereignis oder ein technischer Effekt sein.
2. Missingness kann strukturell sein.
3. Technisch verschiedene Zeilen können dieselbe Fahrt repräsentieren.
4. Fachlich ähnliche Zeilen können unterschiedliche finanzielle Ereignisse repräsentieren.
5. Deshalb benötigen Nachfrage und Umsatz unterschiedliche Regeln.

## 1. Ausgangslage prüfen

```python
from pathlib import Path
import pandas as pd

ROOT = Path.cwd()
while not (ROOT / "data/input/trips_case_initial.parquet").exists():
    if ROOT == ROOT.parent:
        raise FileNotFoundError("Repository-Wurzel nicht gefunden")
    ROOT = ROOT.parent

df = pd.read_parquet(ROOT / "data/input/trips_case_initial.parquet")
df.shape
```

Erwartetes Ergebnis:

| Merkmal | Wert |
|---|---:|
| Zeilen | 200'900 |
| Spalten | 24 |
| Zeilen aus dem offiziellen Sample | 200'000 |
| kontrolliert ergänzte Replay-Zeilen | 900 |
| vorgesehener Trainingszeitraum | 1.–24. Juli 2025 |

Die Pickup-Zeit reicht tatsächlich von `2009-01-01 08:52:26` bis `2025-07-24 23:59:56`. Das Jahr 2009 ist ein erster Hinweis, aber noch keine vollständige Qualitätsentscheidung. Ausserhalb des erwarteten Monats liegen sowohl ungültige Fälle als auch wenige legitime Fahrten über eine Monatsgrenze.

### Moderationsfrage

«Welche Zahl beschreibt hier Fahrten: Zeilen, eindeutige IDs, Signaturen oder etwas anderes?»

Die Antwort wird bewusst noch offengelassen.

## 2. Missingness als Muster

Fünf Felder bilden denselben Nullblock:

```python
missing_block = [
    "passenger_count",
    "RatecodeID",
    "store_and_fwd_flag",
    "congestion_surcharge",
    "Airport_fee",
]

all_missing = df[missing_block].isna().all(axis=1)
pd.crosstab(df["payment_type"], all_missing, margins=True)
```

Erwartete Auflösung:

- In jedem der fünf Felder fehlen **52'540 Werte**, entsprechend rund **26.15 %** der Zeilen.
- Die Werte fehlen gemeinsam.
- **100 %** dieser Nullblock-Zeilen haben `payment_type = 0`.
- Umgekehrt besitzen alle Zeilen mit `payment_type = 0` diesen Nullblock.

`payment_type = 0` steht im Case für Flex Fare beziehungsweise eine Quellenvariante, in der diese Felder nicht geliefert werden. Die Missingness ist somit strukturell und nicht zufällig.

### Entscheidung

Kein pauschales `dropna()`. Die Zeilen bleiben erhalten. Die Missingness wird als Quellenmerkmal dokumentiert; eine Imputation ist für die hier verfolgten Ziele weder nötig noch eindeutig begründbar.

### Häufiger Fehler

Ein KI-generiertes `df.dropna()` würde mehr als ein Viertel des Datensatzes entfernen und eine bestimmte Zahlungsart vollständig ausschliessen. Genau diese Auswirkung muss vor jeder Löschoperation geprüft werden.

## 3. Drei Bedeutungen von «Duplikat»

### Vollständig identische Zeilen

Der Vergleich über alle 24 Felder findet die fachlichen Replays nicht zuverlässig, weil `ingest_record_id`, `ingested_at`, `source_file` und `batch_id` gerade die unterschiedlichen Ingest-Ereignisse beschreiben.

### Gleiche technische ID

`ingest_record_id` ist eindeutig. Das beweist nur, dass jedes Laden eine eigene technische ID erhalten hat, nicht dass jede Zeile eine neue Fahrt ist.

### Identischer Quellpayload

Für den Payloadvergleich werden die 20 fachlichen Quellfelder verwendet; die vier technischen Lineage-Felder bleiben ausserhalb des Vergleichs:

```python
SOURCE_COLUMNS = [
    "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime",
    "passenger_count", "trip_distance", "RatecodeID",
    "store_and_fwd_flag", "PULocationID", "DOLocationID",
    "payment_type", "fare_amount", "extra", "mta_tax", "tip_amount",
    "tolls_amount", "improvement_surcharge", "total_amount",
    "congestion_surcharge", "Airport_fee", "cbd_congestion_fee",
]

df["is_payload_duplicate_copy"] = df.duplicated(
    subset=SOURCE_COLUMNS,
    keep="first",
)
```

Ergebnis: **751 Payload-Kopien**.

Davon sind 750 kontrolliert ergänzte exakte Replays. Ein weiterer Kandidat stammt bereits aus dem offiziellen Sample. Seine Existenz ist didaktisch wichtig: Nicht jede gefundene Kopie gehört automatisch zum kontrollierten Vorfall, und die Lineage darf nicht gelöscht werden.

## 4. Zusammengesetzte Fahrtsignatur und Gegenbuchungen

Der Datensatz enthält keine verlässliche fachliche Trip-ID. Die Referenzlösung bildet deshalb eine Signatur aus:

- Anbieter;
- Pickup- und Dropoff-Zeit;
- Fahrgastzahl und Distanz;
- Tarif- und Store-and-forward-Angabe;
- Pickup- und Dropoff-Zone;
- Zahlungsart.

Finanzbeträge werden zunächst **nicht** in die Signatur aufgenommen. Dadurch bleiben Gruppen sichtbar, deren Fahrtdaten übereinstimmen, deren Beträge aber unterschiedliche Vorzeichen haben.

Erwartete Ergebnisse:

| Befund | Anzahl |
|---|---:|
| Signaturen mit mehr als einer Zeile | 1'206 |
| Gruppen mit positivem und negativem `total_amount` | 405 |

Diese 405 Gruppen sind Hinweise auf finanzielle Gegenbuchungen. Sie dürfen nicht wie technische Duplikate behandelt werden.

### Fachliche Entscheidung

- Für **Nachfrage** repräsentiert ein positives/negatives Paar nicht zwei physische Fahrten.
- Für **Umsatz** bleiben beide Ereignisse relevant, da erst ihre Summe die Nettowirkung zeigt.
- Die Begriffe «Fahrt» und «finanzielles Ereignis» werden ab hier getrennt verwendet.

## 5. Near-Duplicates mit Blocking und Toleranzen

Der kontrollierte Vorfall betrifft Fahrten vom **Freitag, 18. Juli 2025, 17:00–21:00 Uhr**. Die Wiederverarbeitung trifft am **Montag, 21. Juli 2025, ab 09:00 Uhr** ein.

Unter den 900 Replay-Zeilen befinden sich:

| Variante | Anzahl |
|---|---:|
| exakt gleicher Quellpayload | 750 |
| leicht veränderter Payload | 150 |

Bei den 150 Near-Duplicates wurden kontrolliert einzelne Werte um kleine Beträge verändert:

- Zeitstempel um bis zu 2 Sekunden;
- Distanz um 0.01 Meilen;
- Trinkgeld beziehungsweise Gesamtbetrag um 0.01.

Die Referenzlösung blockt über `VendorID`, `PULocationID`, `DOLocationID` und `payment_type`. Innerhalb dieser Gruppen wird der zeitlich nächste offizielle Datensatz gesucht.

```python
blocking = ["VendorID", "PULocationID", "DOLocationID", "payment_type"]

matches = pd.merge_asof(
    later.sort_values("tpep_pickup_datetime"),
    official.sort_values("tpep_pickup_datetime"),
    on="tpep_pickup_datetime",
    by=blocking,
    tolerance=pd.Timedelta(seconds=5),
    direction="nearest",
    suffixes=("_later", "_first"),
)

is_match = (
    matches["ingest_record_id_first"].notna()
    & (matches["tpep_dropoff_datetime_later"]
       - matches["tpep_dropoff_datetime_first"]).abs().le(pd.Timedelta(seconds=5))
    & (matches["trip_distance_later"]
       - matches["trip_distance_first"]).abs().le(0.02)
    & (matches["total_amount_later"]
       - matches["total_amount_first"]).abs().le(0.02)
)
```

Damit werden alle **900 später eingetroffenen Kandidaten** einem ursprünglichen Ereignis zugeordnet. Die Datei-, Batch- und Ingestion-Lineage bestätigt anschliessend den gemeinsamen Replay-Kontext.

### Warum dies nicht nur «fuzzy matching» ist

Die Toleranzen werden fachlich begründet und erst nach Blocking angewendet. Ohne Blocking könnten zwei reale Taxifahrten in einer stark frequentierten Zone zufällig ähnlich aussehen. Ohne Lineage wäre die technische Replay-Erklärung weniger belastbar.

## 6. Zielabhängige Regeln

| Fall | Nachfragesicht | Umsatzsicht | Begründung |
|---|---|---|---|
| kanonisches positives Fahrtereignis | behalten | behalten | physische Fahrt und finanzielles Ereignis |
| technischer Replay | nicht erneut zählen | nicht erneut zählen | wiederholte Verarbeitung |
| negative Gegenbuchung | nicht als zusätzliche Fahrt zählen | behalten | Nettoumsatz benötigt beide Vorzeichen |
| ungeklärte ähnliche Gruppe | prüfen | prüfen | Evidenz reicht nicht für automatische Entscheidung |

Die operative Umsetzung erfolgt zunächst über Flags. Keine Quellzeile wird aus dem Rohbestand gelöscht.

## 7. Übergabe-Checkpoint

`data/checkpoints/checkpoint_01_resolved_events.parquet` soll alle 200'900 Ausgangszeilen plus nachvollziehbare Merkmale enthalten. Empfohlene Zusatzfelder:

- `signature_id`;
- `is_payload_duplicate_copy`;
- `is_replay_batch`;
- `replay_canonical_id` oder eine entsprechende Zuordnung;
- `is_reversal_group`;
- `reversal_role` mit `positive`, `negative` oder `none`;
- Entscheidungsgrund beziehungsweise Match-Evidenz.

Der Checkpoint ist ein **angereicherter, auditierbarer Bestand**, keine endgültig verkleinerte Clean Table. Dadurch bleiben in Aufgabe 2 alle Rohbeobachtungen und Qualitätsentscheidungen prüfbar.

## 8. KI-Retrospektive

Ein guter Prompt nennt:

- das fachliche Ziel;
- die Bedeutung technischer Metadaten;
- die Trennung von Fahrt und Finanzereignis;
- tolerierbare Abweichungen;
- erwartete Tests und Diagnoseausgaben.

Ein problematischer KI-Vorschlag ist an mindestens einem dieser Muster erkennbar:

- `drop_duplicates()` ohne `subset` und ohne Definition;
- `dropna()` ohne Missingness-Analyse;
- negative Beträge pauschal löschen;
- paarweiser Vergleich aller Zeilen;
- Matchscore ohne Stichproben- oder Grenzfallprüfung;
- irreversible Überschreibung des Rohdatensatzes.

## Kernaussage für den Abschluss

Eine technische Zeile ist zunächst ein Ingest-Ereignis. Ob sie eine neue Fahrt, ein Replay oder eine Gegenbuchung repräsentiert, ergibt sich erst aus Payload, Toleranzen, Lineage und Analysezweck.
