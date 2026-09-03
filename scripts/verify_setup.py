#!/usr/bin/env python3
"""Prüft Laufzeit, Kernbibliotheken und Zugriff auf die Workshopdaten."""

from __future__ import annotations

import importlib
import hashlib
import json
import platform
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "input" / "trips_case_initial.parquet"
MANIFEST_PATH = ROOT / "data" / "input" / "manifest.json"

IMPORTS = {
    "numpy": "numpy",
    "pandas": "pandas",
    "pyarrow": "pyarrow",
    "scikit-learn": "sklearn",
    "matplotlib": "matplotlib",
    "seaborn": "seaborn",
    "IPython": "IPython",
}

EXPECTED_COLUMNS = {
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "RatecodeID",
    "store_and_fwd_flag",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "Airport_fee",
    "cbd_congestion_fee",
    "ingest_record_id",
    "ingested_at",
    "source_file",
    "batch_id",
}


def fail(message: str) -> None:
    print(f"SETUP FEHLER: {message}", file=sys.stderr)
    raise SystemExit(1)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if sys.version_info[:2] != (3, 12):
        fail(f"Python 3.12 erwartet, gefunden: {platform.python_version()}")

    versions: dict[str, str] = {}
    modules: dict[str, object] = {}
    for package_name, import_name in IMPORTS.items():
        try:
            module = importlib.import_module(import_name)
        except ImportError as exc:
            fail(f"Bibliothek nicht importierbar: {package_name} ({exc})")
        modules[package_name] = module
        versions[package_name] = getattr(module, "__version__", "installiert")

    if not DATA_PATH.exists():
        fail(f"Ausgangsdaten fehlen: {DATA_PATH.relative_to(ROOT)}")
    if not MANIFEST_PATH.exists():
        fail(f"Datenmanifest fehlt: {MANIFEST_PATH.relative_to(ROOT)}")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if DATA_PATH.stat().st_size != manifest["bytes"]:
        fail("Dateigrösse des Ausgangsdatensatzes stimmt nicht mit dem Manifest überein")
    if sha256(DATA_PATH) != manifest["sha256"]:
        fail("SHA-256 des Ausgangsdatensatzes stimmt nicht mit dem Manifest überein")

    pd = modules["pandas"]
    frame = pd.read_parquet(DATA_PATH)
    missing_columns = sorted(EXPECTED_COLUMNS.difference(frame.columns))
    if missing_columns:
        fail("Fehlende Spalten: " + ", ".join(missing_columns))
    if len(frame) != manifest["rows"]:
        fail(f"{manifest['rows']} Zeilen erwartet, gefunden: {len(frame)}")
    if len(frame.columns) != manifest["columns"]:
        fail(f"{manifest['columns']} Spalten erwartet, gefunden: {len(frame.columns)}")
    if frame["ingest_record_id"].isna().any():
        fail("ingest_record_id enthält Nullwerte")

    print(f"Python: {platform.python_version()}")
    print("Bibliotheken:")
    for package_name, version in versions.items():
        print(f"  {package_name}: {version}")
    print(f"Daten: {DATA_PATH.relative_to(ROOT)}")
    print(f"Form: {len(frame):,} Zeilen × {len(frame.columns)} Spalten")
    print("SETUP OK")


if __name__ == "__main__":
    main()
