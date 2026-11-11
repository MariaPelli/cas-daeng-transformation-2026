# Daten im Workshop

Die folgenden Ordner gehören zum Taxifall (Aufgaben 1–3). Die vier CSV-Dateien für Aufgabe 0 liegen [direkt bei der Aufgabe](../tasks/00_compatibility_and_integration/data/).

## Ordner

| Ordner | Zweck | Versionskontrolle |
| --- | --- | --- |
| `input/` | Unveränderter Ausgangsdatensatz des Cases | ja |
| `reference/` | Lookup-Tabellen und externe Kontextdaten | ja |
| `checkpoints/` | Nach jedem Block freigegebene, geprüfte Zwischenstände | ja |
| `work/` | Eigene Exporte und Zwischenergebnisse | nein |

## Ausgangsdatensatz

`input/trips_case_initial.parquet` enthält fachliche Felder aus den offiziellen
NYC TLC Yellow Taxi Trip Records sowie vier didaktisch ergänzte technische
Metadatenfelder. Der Datensatz wird während des Workshops nie überschrieben.

| Feld | Bedeutung |
| --- | --- |
| `VendorID` | Technologieanbieter des Datensatzes |
| `tpep_pickup_datetime` | Zeitpunkt, zu dem das Taxameter eingeschaltet wurde |
| `tpep_dropoff_datetime` | Zeitpunkt, zu dem das Taxameter ausgeschaltet wurde |
| `passenger_count` | Gemeldete Anzahl Fahrgäste |
| `trip_distance` | Gemeldete Distanz in Meilen |
| `RatecodeID` | Finaler Tarifcode |
| `store_and_fwd_flag` | Hinweis auf zeitversetzte Übermittlung |
| `PULocationID` | Pickup-Zone |
| `DOLocationID` | Dropoff-Zone |
| `payment_type` | Zahlungsart |
| `fare_amount` | Zeit- und distanzabhängiger Fahrpreis |
| `extra` | Weitere Zuschläge |
| `mta_tax` | MTA-Abgabe |
| `tip_amount` | Erfasstes Trinkgeld |
| `tolls_amount` | Mautsumme |
| `improvement_surcharge` | Improvement Surcharge |
| `total_amount` | Gesamtbetrag ohne Cash-Tip |
| `congestion_surcharge` | Congestion Surcharge |
| `Airport_fee` | Flughafen-Gebühr |
| `cbd_congestion_fee` | CBD Congestion Fee |
| `ingest_record_id` | Eindeutige technische ID des Ingest-Ereignisses |
| `ingested_at` | Ankunftszeit im Zielsystem |
| `source_file` | Technische Herkunftsdatei |
| `batch_id` | Technischer Ingest-Batch |

## Herkunft und Transparenz

- Quelle: [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- Dokumentation: [Yellow Taxi Trip Data Dictionary](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)
- Der Organisationname «MetroPulse Operations» und der Managementauftrag sind
  fiktional.
- Der Workshopdatensatz enthält didaktisch vorbereitete technische Ereignisse.
  Die genaue Auflösung wird blockweise in den Walkthroughs veröffentlicht.

