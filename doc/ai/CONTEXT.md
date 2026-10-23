# Kontextindex und Quellenhierarchie

## Lesestrategie

1. `AGENTS.md` und diese Datei für Regeln und Orientierung lesen.
2. `PROJECT.md` bei Fragen zu Ziel, Rolle, Einschränkungen und Erfolgskriterien heranziehen.
3. Bei Codeänderungen betroffene Dateien, Tests und einschlägige Konventionen verifizieren; aktuellen Branch und Commit prüfen.
4. Für Architekturfragen `ARCHITECTURE.md` und einschlägige ADRs verwenden.
5. Für Planung `ROADMAP.md`, für letzte dokumentierte Fortschritte `STATUS.md`, für MCP und Tools `TOOLS.md` konsultieren.
6. Bei fachlichen Recherchefragen und aktivierter Wissensbasis zuerst `../../knowledge/wiki/index.md`, anschließend relevante Wiki-Seiten und Originalquellen lesen.
7. Nur benötigte Skills aktivieren; kein pauschales Einlesen aller Wiki-Dateien.

## Quellenhierarchie (aufgabenspezifisch)

- **Ziel, Scope und Regeln:** `PROJECT.md`, `AGENTS.md`, genehmigte ADRs und fachliche Spezifikationen.
- **Tatsächliche Softwarefunktion:** Live-GitHub-Repository, Code, Tests, Konfigurations- und CI-Ergebnisse.
- **Fachliche Tatsachen:** Zulässige, kontrollierbare Originalquellen mit Provenienz; Wiki-Seiten sind sekundäre, potenziell überholte Synthesen.
- **Planung und Arbeitsstand:** `ROADMAP.md` und `STATUS.md` als datierte Dokumentation.
- **Chatverläufe:** Hinweise und Arbeitsgedächtnis; niemals ohne Bestätigung verifizierte Ist-Dokumentation.

Bei Konflikten keine stillschweigende Quelle als universell autoritativ behandeln; nach Zuständigkeit, Aktualität und Beleglage entscheiden und verbleibende Konflikte sichtbar machen.

## Kontext nach Aufgabentyp

| Aufgabe | Primäre Quellen |
| --- | --- |
| Projektziel / Vorgaben | PROJECT, AGENTS, relevante ADRs |
| Neues Feature | PROJECT, ARCHITECTURE, CONVENTIONS, betroffener Code |
| Bugfix | Fehlermeldung, reproduzierbarer Test, betroffener Code |
| Review | Diff, Tests, CONVENTIONS, ADRs |
| Release | VERSION, CHANGELOG, STATUS, CI |
| Planung | PROJECT, STATUS, ROADMAP |
| Fachliche Recherche | Knowledge-Index, Wiki-Seite, Originalquelle |
| Quellenaufnahme | Knowledge-Schema, Manifest, vorhandene Wiki-Seiten |
| Wiki-Qualitätsprüfung | Knowledge-Schema, manifestierte Quellen, Index |
| Tool/MCP | TOOLS, clientabhängige Konfigurationen |

## Trennung von Projektkontext und LLM Wiki

`doc/ai/` enthält verbindliche Normen, Architektur, Entscheidungen und Fortschrittsdokumentation. Die optionale Struktur `../../knowledge/` enthält nachvollziehbare Rohquellen und abgeleitete Wiki-Seiten. Ein Wiki-Ingest darf keine Anforderungen, ADRs oder Sicherheitsvorgaben automatisch ändern.

## ChatGPT

- Die ChatGPT-Projektanweisungen stehen als Kopiervorlage in `CHATGPT_PROJECT.md`.
- Das Repository bindet `AGENTS.md` nicht automatisch in normale ChatGPT-Web-Chats ein.
- Hochgeladene Projektdateien sind Momentaufnahmen und synchronisieren sich nicht automatisch mit GitHub.
- Für Projektisolation bei Bedarf die tatsächlichen ChatGPT-Projekt-/Memory-Einstellungen konfigurieren; Textanweisungen allein ändern sie nicht.
