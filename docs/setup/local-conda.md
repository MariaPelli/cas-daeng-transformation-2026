# Lokales Setup mit Conda

[← Startseite](../../README.md)

Dieser Weg wird im Unterricht bevorzugt demonstriert. Er eignet sich für
Windows, macOS und Linux.

## Repository herunterladen

Empfohlen ist ein eigener Fork, der lokal geklont wird:

```bash
git clone https://github.com/DEIN-BENUTZERNAME/REPOSITORY-NAME.git
cd REPOSITORY-NAME
```

Alternativ kann das zentrale Workshop-Repository direkt geklont werden. Eigene
Änderungen lassen sich dann lokal committen, aber ohne Schreibberechtigung nicht
in das zentrale Repository pushen.

## Erstinstallation

Im Terminal in den Repository-Ordner wechseln und ausführen:

```bash
conda env create -f environment.yml
conda activate cas-daeng-transformation
python -m ipykernel install --user --name cas-daeng-transformation --display-name "Python (CAS DAENG Transformation)"
python scripts/verify_setup.py
jupyter lab
```

Unter Windows können die Befehle im Anaconda Prompt ausgeführt werden.

## Bestehende Umgebung aktualisieren

Nur wenn sich `environment.yml` während der Vorbereitungsphase geändert hat:

```bash
conda env update -n cas-daeng-transformation -f environment.yml --prune
conda activate cas-daeng-transformation
python scripts/verify_setup.py
```

## Erwartetes Resultat

Am Ende der Prüfung erscheint:

```text
SETUP OK
```

In Jupyter den Kernel **Python (CAS DAENG Transformation)** auswählen.

## Neue Workshopmaterialien laden

Vor dem Aktualisieren die eigene Arbeit speichern und committen. Bei einem Fork
die Änderungen zusätzlich in den eigenen Fork pushen und auf GitHub
**Sync fork → Update branch** wählen. Danach im lokalen Repository ausführen:

```bash
git pull --ff-only
```

Neue Walkthroughs, Musterlösungen und Checkpoints erhalten eigene Dateinamen.
Die bearbeiteten `task.ipynb`-Dateien werden dadurch nicht überschrieben.

Wer Git nicht verwenden möchte, folgt der Anleitung
[`manual-download.md`](manual-download.md).

## Häufige Ursache bei `EnvironmentNameNotFound`

Diese Meldung bedeutet meist, dass die vorherige Erstellung des Environments
abgebrochen ist. Zuerst die Fehlermeldung von `conda env create` beheben und den
Erstellungsbefehl danach erneut ausführen.

[← Startseite](../../README.md)
