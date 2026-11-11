[Workshop-Übersicht](README.md) · [Technische Vorbereitung](README_technical_preparation.md) · [Aufgabe 0: Kompatibilität und Integration](tasks/00_compatibility_and_integration/README.md) · [Aufgabe 1: Datenqualität und Dubletten](tasks/01_data_quality_and_duplicates/README.md) · [Aufgabe 2: Ausreisser und Noise](tasks/02_outliers_and_noise/README.md) · [Aufgabe 3: Rückschätzung und Prognose](tasks/03_forecasting/README.md)

---

# CAS Data Engineering · Transformation

Diese Seite beschreibt ausschliesslich die **technische Vorbereitung** des
Workshops. Die inhaltliche [Workshop-Übersicht](README.md) und die Links zu den
einzelnen Aufgaben befinden sich in der Navigation zuoberst.

Für den Workshop stehen genau zwei gleichwertige Wege zur Verfügung:

- **Weg A:** lokal auf Windows, macOS oder Linux;
- **Weg B:** im Browser mit GitHub Codespaces.

Im Unterricht werden bei Weg A sowohl **JupyterLab** als auch **Visual Studio
Code (VS Code)** demonstriert. Für die Bearbeitung kann anschliessend eines der
beiden Werkzeuge gewählt werden.

## Welcher Weg passt zu mir?

| Kriterium | Weg A: lokal mit Conda | Weg B: GitHub Codespaces |
| --- | --- | --- |
| Einrichtung | Das Conda-Environment wird einmalig auf dem eigenen Rechner erstellt. | Die Umgebung wird beim ersten Start automatisch eingerichtet. |
| Betriebssystem | Windows, macOS und Linux werden unterstützt. | Einheitliche Linux-Umgebung im Browser. |
| Entwicklungsumgebung | JupyterLab oder VS Code. | VS Code im Browser. |
| Rechenleistung | Verwendet Prozessor, Arbeitsspeicher und Speicherplatz des eigenen Rechners. | Verwendet eine Cloud-Maschine von GitHub. |
| Internet | Nach der Installation weitgehend offline nutzbar. | Für die Arbeit und Synchronisation erforderlich. |
| Kosten | Kein Cloud-Kontingent erforderlich. | Persönliches Codespaces-Kontingent; nach dessen Verbrauch können Kosten entstehen oder die Nutzung wird blockiert. |
| Aktualisierung nach einem Block | Mit Git per Pull oder durch manuellen Download der neuen Dateien. | Fork synchronisieren und Änderungen in den Codespace ziehen. |

Wer unsicher ist, kann den im Unterricht primär demonstrierten **Weg A**
wählen. Codespaces ist insbesondere dann praktisch, wenn lokal nichts
installiert werden kann oder soll.

---

## Weg A: lokal mit Conda

Für Weg A gibt es zwei Möglichkeiten, das Repository
`cas-daeng-transformation-2026` auf den eigenen Rechner zu laden:

- **A1: mit Git** – empfohlen, weil neue Workshopdateien einfach nachgeladen
  werden können;
- **A2: als ZIP-Datei** – möglich, wenn Git noch nicht verwendet werden soll.

Die Einrichtung des Conda-Environments ist danach bei A1 und A2 identisch.

### Voraussetzungen

Vor dem Workshop sollten installiert sein:

1. **Miniconda** oder **Anaconda**;
2. **VS Code**;
3. die VS-Code-Erweiterungen **Python** und **Jupyter** von Microsoft;
4. zusätzlich **Git**, falls A1 verwendet wird.

Für die Installation und die erstmalige Erstellung des Environments ist eine
Internetverbindung erforderlich.

### A1: Repository mit Git beziehen

#### 1. Fork erstellen

Das zentrale Workshop-Repository auf GitHub öffnen und oben rechts **Fork**
wählen. Dadurch entsteht eine eigene Kopie des Repositories im persönlichen
GitHub-Konto.

#### 2. Fork klonen

Auf der Startseite des eigenen Forks **Code** wählen und die HTTPS-Adresse
kopieren. Danach ein Terminal öffnen:

- unter Windows den **Anaconda Prompt**;
- unter macOS oder Linux das **Terminal**.

Zuerst in den Ordner wechseln, in dem das Repository abgelegt werden soll.
Pfade mit Leerzeichen müssen in Anführungszeichen stehen.

**Windows – Anaconda Prompt:**

```bat
cd /d "C:\Users\DEIN-NAME\Documents"
```

**macOS:**

```bash
cd "/Users/DEIN-NAME/Documents"
```

**Linux:**

```bash
cd "/home/DEIN-NAME/Documents"
```

Anschliessend den eigenen Fork klonen. Der lokale Ordner erhält dabei ebenfalls
den Namen `cas-daeng-transformation-2026`:

```bash
git clone https://github.com/DEIN-BENUTZERNAME/cas-daeng-transformation-2026.git cas-daeng-transformation-2026
cd cas-daeng-transformation-2026
```

Die Beispieladresse wird dabei durch die zuvor auf GitHub kopierte
HTTPS-Adresse ersetzt.

### A2: Repository manuell als ZIP beziehen

1. Das zentrale Workshop-Repository auf GitHub öffnen.
2. **Code → Download ZIP** wählen.
3. Die ZIP-Datei entpacken.
4. Den entpackten Hauptordner in `cas-daeng-transformation-2026` umbenennen.
5. Den **Anaconda Prompt** unter Windows beziehungsweise das **Terminal** unter
   macOS oder Linux öffnen.
6. In den entpackten Ordner wechseln.

Beispiele für den letzten Schritt:

**Windows – Anaconda Prompt:**

```bat
cd /d "C:\Users\DEIN-NAME\Documents\cas-daeng-transformation-2026"
```

**macOS:**

```bash
cd "/Users/DEIN-NAME/Documents/cas-daeng-transformation-2026"
```

**Linux:**

```bash
cd "/home/DEIN-NAME/Documents/cas-daeng-transformation-2026"
```

Die Pfade sind Beispiele und müssen an den tatsächlichen Speicherort angepasst
werden.

### Conda-Environment erstellen

Die folgenden Schritte gelten für **A1 und A2** sowie für Windows, macOS und
Linux.

Wichtig: Die Befehle müssen im Ordner `cas-daeng-transformation-2026`
ausgeführt werden. Dort befindet sich die Datei `environment.yml`. Dies kann
vorab geprüft werden:

**Windows:**

```bat
dir environment.yml
```

**macOS und Linux:**

```bash
ls environment.yml
```

Danach das Environment erstellen:

```bash
conda env create -f environment.yml
```

Die Auflösung der Abhängigkeiten sowie das Herunterladen und Installieren der
Pakete können je nach Rechner und Internetverbindung **mehrere Minuten** dauern.
Während `Solving environment`, `Downloading and Extracting Packages` oder
`Executing transaction` angezeigt wird, arbeitet Conda weiter. Den Vorgang
nicht vorschnell abbrechen.

Nach erfolgreicher Erstellung das Environment aktivieren, den Jupyter-Kernel
registrieren und die Installation prüfen:

```bash
conda activate cas-daeng-transformation
python -m ipykernel install --user --name cas-daeng-transformation --display-name "Python (CAS DAENG Transformation)"
python scripts/verify_setup.py
```

Die Prüfung war erfolgreich, wenn am Ende Folgendes erscheint:

```text
SETUP OK
```

#### Falls das Environment bereits vorhanden ist

Das Environment muss nicht jedes Mal neu erstellt werden. Wenn sich die Datei
`environment.yml` später ändert, wird es mit folgenden Befehlen aktualisiert:

```bash
conda env update -n cas-daeng-transformation -f environment.yml --prune
conda activate cas-daeng-transformation
python scripts/verify_setup.py
```

### Mit JupyterLab arbeiten

Im Terminal in den Ordner `cas-daeng-transformation-2026` wechseln, falls nötig
das Environment aktivieren und JupyterLab starten:

```bash
conda activate cas-daeng-transformation
jupyter lab
```

JupyterLab öffnet sich normalerweise automatisch im Browser. Danach
`notebooks/00_setup_check.ipynb` öffnen, den Kernel
**Python (CAS DAENG Transformation)** wählen und **Run All** ausführen.

JupyterLab kann im Terminal mit `Ctrl+C` beendet werden.

### Mit VS Code arbeiten

Im Terminal in den Ordner `cas-daeng-transformation-2026` wechseln, falls nötig
das Environment aktivieren und VS Code öffnen:

```bash
conda activate cas-daeng-transformation
code .
```

Der Punkt in `code .` bedeutet: den aktuellen Ordner in VS Code öffnen.

Falls der Befehl `code` nicht erkannt wird, VS Code über das Startmenü oder den
Programme-Ordner öffnen und **File → Open Folder →
cas-daeng-transformation-2026** wählen.

Anschliessend:

1. `notebooks/00_setup_check.ipynb` öffnen;
2. oben rechts **Select Kernel** wählen;
3. **Python (CAS DAENG Transformation)** auswählen;
4. **Run All** ausführen.

Am Ende der lokalen Arbeit kann das Environment im Terminal deaktiviert werden:

```bash
conda deactivate
```

---

## Weg B: GitHub Codespaces

Für diesen Weg werden ein GitHub-Konto und ein noch verfügbares
Codespaces-Kontingent benötigt.

### Codespace erstmals erstellen

1. Das zentrale Workshop-Repository auf GitHub öffnen und **Fork** wählen.
2. Den eigenen Fork öffnen.
3. **Code → Codespaces → Create codespace on main** wählen.
4. Die automatische Einrichtung vollständig abwarten.
5. Warten, bis im Terminal `SETUP OK` erscheint.
6. `notebooks/00_setup_check.ipynb` öffnen.
7. Den Kernel **Python (CAS DAENG Transformation)** wählen und **Run All**
   ausführen.

Beim ersten Start werden das Conda-Environment, alle Python-Pakete und der
Jupyter-Kernel automatisch eingerichtet. Auch dieser Vorgang kann **mehrere
Minuten** dauern. Es müssen dafür keine Installationsbefehle manuell eingegeben
werden.

Codespaces verwendet VS Code im Browser. Die Notebook-Bedienung entspricht
weitgehend der lokalen Nutzung von VS Code.

### Codespace stoppen

Ein Codespace sollte während längerer Pausen und nach der Arbeit gestoppt
werden, damit kein unnötiges Compute-Kontingent verbraucht wird. Eigene
Änderungen vorher committen und in den Fork pushen. Nach Abschluss des
Workshops kann der Codespace gelöscht werden; solange er existiert, kann
Speicherverbrauch anfallen.

---

## Neue Dateien nach einem Workshopblock laden

Aufgaben-Notebooks werden durch spätere Freigaben nicht überschrieben.
Walkthroughs, Musterlösungen und Checkpoints erhalten jeweils neue Dateinamen.

### Mit Git: A1 und Codespaces

Vor der Synchronisation zuerst die eigene Arbeit speichern. Empfohlen ist ein
Commit im eigenen Fork:

```bash
git status
git add .
git commit -m "Eigener Stand nach Block 1"
git push
```

Die Blocknummer in der Commit-Nachricht wird jeweils angepasst. Falls Git beim
ersten Commit nach Name und E-Mail-Adresse fragt, können diese einmalig gesetzt
werden:

```bash
git config --global user.name "Vorname Nachname"
git config --global user.email "name@example.com"
```

Danach:

1. den eigenen Fork auf GitHub öffnen;
2. **Sync fork → Update branch** wählen;
3. zurück in das lokale Terminal beziehungsweise das Codespaces-Terminal
   wechseln;
4. sicherstellen, dass das Terminal im Hauptordner des Repositories steht
   (lokal `cas-daeng-transformation-2026`; in Codespaces wird dieser Ordner
   automatisch geöffnet);
5. die neuen Dateien laden:

```bash
git pull --ff-only
```

In VS Code und Codespaces kann alternativ **Terminal → Run Task → Workshop:
Neue Materialien laden** gewählt werden.

### Ohne Git: A2

Nach jedem Block wird angegeben, welche Dateien neu hinzugekommen sind und in
welchen Unterordner sie gehören. Diese Dateien können auf GitHub einzeln über
**Download raw file** heruntergeladen und am angegebenen Ort innerhalb von
`cas-daeng-transformation-2026` gespeichert werden.

Typische neue Dateien sind:

```text
tasks/NN_name/WALKTHROUGH.md
tasks/NN_name/task_sample_solution.ipynb
data/checkpoints/checkpoint_NN_name.parquet
```

Die eigene `task.ipynb` darf dabei nicht überschrieben werden. Für neue
Walkthroughs, Musterlösungen oder Checkpoints muss das Conda-Environment nicht
neu erstellt werden. Nur wenn ausdrücklich eine aktualisierte
`environment.yml` veröffentlicht wird, ist das Environment mit dem weiter oben
gezeigten Update-Befehl zu aktualisieren.

---

## Technische Ordnerstruktur

```text
.devcontainer/       automatische Codespaces-Konfiguration
.vscode/             gemeinsame VS-Code-Einstellungen und Aufgaben
data/
  input/             unveränderlicher Ausgangspunkt
  reference/         Referenz- und Kontextdaten
  checkpoints/       Zwischenstände für die Folgeaufgaben im Taxifall
  work/              lokale, nicht versionierte Arbeitsergebnisse
docs/setup/           ergänzende technische Hinweise
notebooks/            technische Start- und Prüfnotebooks
scripts/              Hilfs- und Prüfroutinen
tasks/                ein Ordner pro Workshop-Aufgabe
```

## Workshop-Navigation

Die Übersicht über den Transformationstag, die Fallstudie und die einzelnen
Workshopaufgaben ist über die Navigation zuoberst erreichbar.
