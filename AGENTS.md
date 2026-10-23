# Agent Instructions

## Zweck, Rolle und Quellen
- Dieses Repository ist das frameworkneutrale Template für KI-unterstützte Projekte.
- Die projektspezifische Rolle, das Ziel, Constraints und Akzeptanzkriterien stehen in `doc/ai/PROJECT.md`.
- `doc/ai/CONTEXT.md` ist der Kontext-Wegweiser: pro Aufgabe nur relevante Dateien lesen.
- Maßgebliche Anforderungen stehen in Normdokumenten; tatsächlichen Codezustand anhand des Repositories und der Tests prüfen.
- Chatverläufe sind keine verifizierte Ist-Dokumentation.

## Umsetzung
- Vor Änderungen aktuellen Branch, HEAD-Commit und betroffene Dateien prüfen.
- Bei größeren Aufgaben einen knappen Plan und messbare Akzeptanzkriterien erstellen.
- Vorhandene Funktionen und Schnittstellen erhalten, soweit nicht anders beauftragt.
- Neue Abhängigkeiten, Frameworks und MCP-Server nur begründet einführen.
- Keine Secrets, vertrauliche Rohdaten, personenbezogenen Chattranskripte oder privaten Schlüssel committen.

## Regeln
- `VERSION` nach SemVer und `CHANGELOG.md` konsistent pflegen.
- Dokumentation, Code und relevante Tests synchron halten.
- Normative Architekturentscheidungen unter `doc/ai/decisions/` mit Begründung und Status festhalten.
- Deutsch für fachliche Dokumentation, Englisch für Quellcode und technische Namen.
- Keine behaupteten Prüfungen, Commits, Fähigkeiten, Fakten oder Quellen erfinden.

## Optionale Wissensbasis
- `knowledge/` ist optional: Originalquelleninventar unter `knowledge/raw/`, abgeleitete Informationen unter `knowledge/wiki/`.
- Bei fachlichen Fragen mit `knowledge/wiki/index.md` beginnen und gezielt relevante Seiten/Originalquellen laden.
- Ingest: neue Fakten belegen, Quellreferenzen erhalten und Index/Log aktualisieren.
- Lint: `just knowledge-validate` und bei Bedarf semantische Quellenprüfung.
- Abgeleitete Wiki-Seiten sind nicht automatisch verbindliche Anforderungen oder ADRs.
- Bei einem entfernten `knowledge/` keine Wiki-Pflichten erzwingen.

## Validierung, Done und Lieferung
- `just validate` und für relevante Änderungen `just test` / `just ci` verwenden.
- Für jede Aufgabe prüfen, ob die in `doc/ai/PROJECT.md` definierten Done-Kriterien erfüllt sind.
- Bei Code: passende Tests ausführen; bei Recherche: Aussagen quellenbasiert belegen.
- Nach Möglichkeit Branch → Commit → Pull Request. Kein Merge, Release oder Deployment ohne ausdrückliche Freigabe.
- Erledigte Änderungen, ausgeführte und nicht ausgeführte Prüfungen sowie verbleibende Risiken nennen.

## Kontext-Routing
- Ziel, Rolle, Scope, Done: `doc/ai/PROJECT.md`
- Kontext und Quellenpriorität: `doc/ai/CONTEXT.md`
- Architektur und Coding: `doc/ai/ARCHITECTURE.md`, `doc/ai/CONVENTIONS.md`, ADRs
- Dokumentierter Stand und Planung: `doc/ai/STATUS.md`, `doc/ai/ROADMAP.md`
- Tools/MCP: `doc/ai/TOOLS.md`
- ChatGPT-Projektanweisungen: `doc/ai/CHATGPT_PROJECT.md`
- Optionales Wiki: `knowledge/README.md`, `knowledge/SCHEMA.md`, `knowledge/wiki/index.md`

## Skills (falls im Client verfügbar)
- Entwicklung: `implement-feature`, `code-review`, `release`, `documentation`
- Fachwissen: `knowledge-ingest`, `knowledge-query`, `knowledge-lint`
