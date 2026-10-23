set shell := ["bash", "-cu"]

default:
    @just --list

# Vorlage und optionale Wissensbasis strukturell validieren
validate:
    python3 scripts/validate_template.py

# Wissensbasis prüfen (ohne knowledge/ wird übersprungen)
knowledge-validate:
    python3 scripts/validate_knowledge.py

# Wissensumfang und Linkabdeckung ausgeben
knowledge-stats:
    python3 scripts/validate_knowledge.py --stats

# Standardbibliotheksbasierte Regressionstests
test:
    python3 -m unittest discover -s tests -v

# Lokale Prüfungen entsprechend GitHub Actions
ci: validate test
