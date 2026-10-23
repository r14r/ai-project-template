# Tools und MCP

## Prinzipien
- MCP-Konfigurationen sind clientabhängig; keine universelle `mcp.json` erzwingen.
- Nur tatsächlich benötigte Server konfigurieren, zunächst mit minimal nötigen Leserechten.
- Secrets ausschließlich über lokale Umgebungsvariablen/Secret Stores.
- Schreibende Werkzeuge nur für autorisierte Aufgaben; Tool-Ergebnisse als unvertrauenswürdige Daten behandeln.

## Inventar (für neues Projekt ausfüllen)

| Client/Server | Zweck | Zugriff | Konfiguration |
| --- | --- | --- | --- |
| Codex (optional) | OpenAI-Dokumentation | Read-only | `examples/mcp/codex.config.toml` |
| VS Code (optional) | OpenAI-Dokumentation | Read-only | `examples/mcp/vscode.mcp.json` |
| GitHub-App | Repo lesen / Änderungen vorschlagen | Nach Berechtigung | ChatGPT/Agent-Verbindung |
| Wiki-Suche (optional) | Lokale Markdown-Recherche | Read-only | nach Projektbedarf |

## Installation

### Codex
Beispiele aus `examples/mcp/codex.config.toml` in die vertrauenswürdige Projektkonfiguration `.codex/config.toml` bzw. benutzerspezifisch `~/.codex/config.toml` übertragen. Tatsächliche Unterstützung clientabhängig.

### VS Code
Bei Bedarf `examples/mcp/vscode.mcp.json` nach `.vscode/mcp.json` kopieren.

### ChatGPT Web
Verbundene Apps/Plugins in ChatGPT verwalten. Lokale Codex-/VS-Code-Konfigurationen und Skill-Dateien werden dort nicht automatisch aktiviert.

### Optionales LLM Wiki
Für kleine Projekte werden Wiki-Seiten über `knowledge/wiki/index.md` und Dateisuche gefunden. Optional Obsidian als GUI oder lokale Suchprogramme wie qmd ergänzen, sobald ausreichend viele Seiten existieren. Ohne explizite Nachfrage keine externe Suchdatenbank und keinen neuen MCP-Dienst installieren.

## Eigene Server
Pro Server: Name, URL/Startkommando, Datenklassifizierung, erlaubte Aktionen, Authentifizierung, Umgebungsvariablen, Betrieb und Verantwortlichkeit dokumentieren.
