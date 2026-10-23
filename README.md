# AI Project Template

Frameworkneutrale, versionierte Vorlage für die Zusammenarbeit zwischen **ChatGPT-Projekten**, **GitHub-Repositories** und Coding-Agents (z. B. Codex und VS Code).

## Architektur: Regeln, Kontext, Workflows, Wissen

Das GitHub-Repository ist die maßgebliche Quelle für Projektvorgaben, Quellcode, Architektur, Entscheidungen und verifizierten Arbeitsstand. ChatGPT ist die Arbeitsoberfläche; Projektdateien sind ohne Live-GitHub-Zugriff lediglich hochgeladene Momentaufnahmen.

| Ebene | Einstieg | Aufgabe |
| --- | --- | --- |
| Projektanweisungen | [doc/ai/CHATGPT_PROJECT.md](doc/ai/CHATGPT_PROJECT.md) | Rolle, Goal, Context, Constraints, Done when, Arbeitsweise |
| Regeln | [AGENTS.md](AGENTS.md) | Verbindliche Agent-Regeln und Kontext-Routing |
| Projektkontext | [doc/ai/](doc/ai/) | Ziel, Architektur, Konventionen, Status, Roadmap, ADRs |
| Skills | [.agents/skills/](.agents/skills/) | Aufgabenbezogene, wiederverwendbare Agent-Workflows |
| MCP | [doc/ai/TOOLS.md](doc/ai/TOOLS.md) und [examples/mcp/](examples/mcp/) | Optionale, clientabhängige externe Werkzeuge |
| LLM Wiki (optional) | [knowledge/](knowledge/) | Originalquellen plus KI-gepflegte, belegte Synthesen |
| Validierung | [scripts/](scripts/) | Struktur-, Quellen-/Linkprüfungen und Tests |

## Neues Projekt aufsetzen

1. In den GitHub-Einstellungen dieses Repositories einmalig **Template repository** aktivieren (sofern noch nicht aktiviert).
2. **Use this template** wählen und ein neues Repository erzeugen oder die Dateien gezielt in ein bestehendes Repository übernehmen.
3. In [PROJECT.md](doc/ai/PROJECT.md) Name, Rolle, exaktes Ziel, Scope, Constraints, Akzeptanzkriterien und kanonisches Repository eintragen.
4. [CONTEXT.md](doc/ai/CONTEXT.md), Architektur, Konventionen, STATUS und ROADMAP anpassen. Platzhalter und nicht zutreffende Skills entfernen.
5. [CHATGPT_PROJECT.md](doc/ai/CHATGPT_PROJECT.md) als Vorlage in **ChatGPT → Projekt → Projektanweisungen** einfügen. `PROJECT.md` und `CONTEXT.md` dort als Quellen verfügbar machen; GitHub-Verbindung bei Bedarf aktivieren.
6. Falls eine isolierte Projekt-Historie nötig ist, die tatsächlich verfügbaren Projekteinstellungen für projektbezogene Erinnerung konfigurieren. Ein Satz in Projektanweisungen ersetzt diese Einstellung nicht.
7. Für optionale MCP-Konfigurationen Beispiele aus `examples/mcp/` in den jeweiligen Client übertragen; Secrets nicht im Repository speichern.
8. Die optionale Wissensbasis aktivieren, indem `knowledge/` beibehalten und nach [SCHEMA.md](knowledge/SCHEMA.md) gepflegt wird; andernfalls den gesamten Ordner löschen.
9. Mit `just ci` validieren (oder die untenstehenden Python-Befehle direkt ausführen).

Die Dateien `AGENTS.md`, Skills und lokale MCP-Konfigurationen werden **nicht automatisch** durch normales ChatGPT Web geladen. Zugriff und Aktivierung hängen von Client und den verfügbaren Verbindungen ab.

## Alltag mit einem Agent

1. `AGENTS.md` und `doc/ai/CONTEXT.md` zur Orientierung lesen.
2. Aufgabe als Entwicklung, Recherche, Ingest, Review oder Release einstufen.
3. Nur benötigte Dokumente/Dateien und Skills laden.
4. Vor Codeänderungen Branch, Commit, betroffene Quelltexte und Tests prüfen.
5. Für Fachwissen zuerst den Wiki-Index und anschließend Originalquellen konsultieren.
6. Ergebnis gegen `PROJECT.md` und Definition of Done validieren.
7. Bei Änderungen Status, Wiki-Index/Log und ADRs **nur entsprechend ihrer Zuständigkeit** aktualisieren; Änderungen über PR zur Freigabe bereitstellen.

## Befehle

```bash
just validate            # Template + optionale Wiki-Struktur
just test                # Python-Regressionstests
just ci                  # Validate + Tests
just knowledge-validate  # Wiki-Provenienz und Links
just knowledge-stats     # Quellen-, Seiten- und Indexstatistik
```

Ohne `just` direkt:

```bash
python3 scripts/validate_template.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_knowledge.py --stats
```

Python 3.11+ erforderlich (stdlib `tomllib`). Externe Pakete, Backend, Datenbank und Docker sind für dieses Template nicht erforderlich.

## Struktur

```text
AGENTS.md
.agents/skills/{implement-feature,code-review,release,documentation}/SKILL.md
.agents/skills/{knowledge-ingest,knowledge-query,knowledge-lint}/SKILL.md
.github/workflows/ci.yml
doc/ai/{PROJECT,CONTEXT,ARCHITECTURE,CONVENTIONS,STATUS,ROADMAP,CHATGPT_PROJECT,TOOLS}.md
doc/ai/decisions/
knowledge/                    # vollständig optional
  README.md, SCHEMA.md
  raw/manifest.yaml, raw/sources/
  wiki/index.md, wiki/log.md
  wiki/{concepts,entities,topics,syntheses}/
examples/mcp/{codex.config.toml,vscode.mcp.json}
scripts/{validate_template.py,validate_knowledge.py}
tests/test_validate_knowledge.py
justfile, VERSION, CHANGELOG.md
```

## Quellentreue und Sicherheit

- `doc/ai/` enthält bindende Ziele, Architektur und Status. Wiki-Seiten sind abgeleitetes Fachwissen und verändern diese Vorgaben nicht automatisch.
- Originalquellen nicht unbemerkt ändern. Externe Quelle ggf. als URI und SHA-256 erfassen.
- Wiki-Artikel benötigen eindeutige IDs, Status, Datum und referenzierte Quellen. `reviewed` nur nach tatsächlicher Prüfung setzen.
- Die CI prüft Syntax, Quellreferenzen und Links, **nicht** fachliche Wahrheit.
- Keine vertraulichen Quellen, Secrets oder personenbezogenen Chattranskripte ohne Berechtigung in Git übernehmen.
- Obsidian oder Suchwerkzeuge wie qmd sind optional; kein RAG-Backend erforderlich.
- `AGENTS.md` (Plural) ist die übliche Codex-Regeldatei; der Singular ist kein gleichwertiger Ersatz.
