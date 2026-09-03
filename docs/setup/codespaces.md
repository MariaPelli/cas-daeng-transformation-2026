# Setup mit GitHub Codespaces

[← Startseite](../../README.md)

## Codespace erstellen

1. Das Workshop-Repository auf GitHub forken.
2. Im eigenen Fork **Code → Codespaces → Create codespace on main** wählen.
3. Die automatische Einrichtung vollständig abwarten.
4. Prüfen, ob im Terminal `SETUP OK` erscheint.
5. `notebooks/00_setup_check.ipynb` öffnen.
6. Den Kernel **Python (CAS DAENG Transformation)** wählen und **Run All**
   ausführen.

Beim ersten Start wird das Conda-Environment automatisch aus `environment.yml`
erstellt. Dafür sind keine Installationsbefehle im Terminal erforderlich.

GitHub stellt für persönliche Konten ein monatliches Freikontingent bereit. Ein
Zahlungsmittel ist für die Nutzung innerhalb dieses Kontingents nicht nötig.
Ist das Kontingent aufgebraucht und übernimmt keine Organisation die Kosten,
wird die weitere Nutzung ohne Zahlungsmittel blockiert. Der aktuelle Stand ist
in der [GitHub-Dokumentation zur Codespaces-Abrechnung](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces)
beschrieben.

Da die Teilnehmenden mit einem Fork arbeiten, wird der Codespace im Regelfall
dem persönlichen Konto belastet. Eine Organisation übernimmt die Kosten nur,
wenn sie dies für Mitglieder oder externe Mitarbeitende ausdrücklich erlaubt
hat.

## Neue Workshopmaterialien laden

Nach der Freigabe eines Walkthroughs:

1. Eigene Änderungen committen und in den Fork pushen.
2. Auf GitHub im Fork **Sync fork → Update branch** wählen.
3. Im Codespace die VS-Code-Aufgabe **Workshop: Neue Materialien laden**
   ausführen oder in Source Control **Pull** wählen.

Da Musterlösungen, Walkthroughs und Checkpoints unter neuen Dateinamen
hinzukommen, werden die bearbeiteten `task.ipynb`-Dateien nicht überschrieben.

## Kontingent schonen

- Für den Workshop genügt der voreingestellte 2-Kern-Codespace.
- Codespace bei Pausen stoppen; so endet der Compute-Verbrauch.
- Eigene Änderungen regelmässig committen und pushen.
- Den Codespace nach Abschluss des Workshops löschen; solange er existiert,
  wird Speicherverbrauch erfasst.

## Codespace neu aufbauen

Eine Änderung an `environment.yml` oder `.devcontainer/devcontainer.json` wird
in einem bestehenden Codespace über die Command Palette und
**Codespaces: Rebuild Container** übernommen. Während des Workshoptags soll dies
nicht erforderlich sein.

[← Startseite](../../README.md)
