# Optionale Projekt-Wissensbasis

Die Wissensbasis erweitert den verbindlichen Projektkontext in `doc/ai/` um eine quellenbasierte, langfristig gepflegte Markdown-Wiki-Schicht (LLM Wiki).

## Grenzen
- `doc/ai/` und `AGENTS.md` bleiben für Ziele, Regeln, Architektur und Entscheidungen maßgeblich.
- `knowledge/raw/` inventarisiert Originalquellen; die Originale werden nicht unbemerkt verändert.
- `knowledge/wiki/` enthält abgeleitete, zitierbare Erkenntnisse, keine automatisch verbindlichen Anforderungen.
- Für kleine Projekte kann `knowledge/` vollständig entfallen. Alle Knowledge-Checks überspringen diese Schicht dann.
- Keine Secrets, personenbezogene Chattranskripte oder nicht freigegebene vertrauliche Quellen übernehmen.

## Einstieg
1. Quellen in `raw/manifest.yaml` erfassen (oder auf externe, kontrolliert zugängliche Quellen verweisen).
2. Bei fachlichen Fragen zuerst `wiki/index.md` lesen und nur relevante Seiten öffnen.
3. Wiki-Seiten gemäß `SCHEMA.md` erstellen; belegte Aussagen eindeutig Quellen zuordnen.
4. Änderungen in `wiki/log.md` protokollieren und `wiki/index.md` aktualisieren.
5. Mit `just knowledge-validate` die Struktur prüfen; `just knowledge-stats` zeigt Kennzahlen.

## Skills
- `knowledge-ingest`: neue Originalquellen kontrolliert integrieren.
- `knowledge-query`: Fragen quellenbasiert beantworten.
- `knowledge-lint`: formale Prüfung und semantische Risikoliste.

## Erweiterungen
Obsidian und eine lokale Suchlösung (z. B. qmd) sind bei großen Wissensbasen optional; kein MCP-Server oder Vektorindex ist verpflichtend.
