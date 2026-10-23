# Wissensschema (Version 1)

Die Dateistruktur ist bewusst einfach, Git-kompatibel und ohne zusätzliche Python-Pakete validierbar.

## Originalquellen

`raw/manifest.yaml` enthält `sources:` mit Einträgen in der Form:

```yaml
sources:
  - id: official-api-docs
    title: Official API documentation
    uri: https://example.org/api
    retrieved: 2026-10-23
    sha256: ""
```

Pflichtfelder: eindeutige `id`, `title`, `uri`. Bei lokalen Dateien ist `uri` ein relativer Pfad unter `raw/` (z. B. `sources/reference.md`); externe URI können `https://` nutzen. Das Beispieldokument hier ist keine tatsächliche Quelle und darf nicht ungeprüft übernommen werden. Zusätzliche Felder: `retrieved` (ISO-Datum), `sha256` zur Integritätsprüfung.

Der stdlib-Validator akzeptiert die gezeigte flache YAML-Teilmenge, kein beliebiges YAML. Quell-ID: `[a-z0-9][a-z0-9._-]*`. Große Binärquellen bevorzugt extern und mit nachvollziehbarer URI/Prüfsumme verwalten.

## Wiki-Seiten

Markdown-Seiten in `wiki/concepts/`, `wiki/entities/`, `wiki/topics/`, `wiki/syntheses/` haben YAML-Frontmatter:

```yaml
---
id: example-concept
title: Example Concept
type: concept
status: draft
updated: 2026-10-23
sources:
  - official-api-docs
related:
  - ../topics/example-topic.md
---
```

Pflichtfelder: `id`, `title`, `type`, `status`, `updated`, `sources`, `related`.
Gültige Typen: `concept`, `entity`, `topic`, `synthesis` (passend zum Verzeichnis).
Gültige Status: `draft`, `reviewed`, `disputed`, `stale`.
Listen können mehrzeilig oder `[]` sein. Die Quellen-ID muss im Manifest vorhanden sein; `related` enthält relative Markdown-Links ab der Wiki-Seite. `updated` ist ein ISO-Datum.

Für inhaltliche Aussagen unterhalb des Frontmatters Quellenbelege (ID und optional genauer Abschnitt) nennen. Bei widersprüchlichen Quellen Konflikt und unterschiedliche Positionen explizit dokumentieren. `reviewed` bedeutet fachlich überprüft und darf nicht allein durch das Modell behauptet werden.

## Indizes und Log

- `wiki/index.md`: kurzer, manuell/agentisch gepflegter Wegweiser mit Links zu allen Wiki-Seiten.
- `wiki/log.md`: chronologisches Protokoll der Ingest-, Query- und Lint-Aktivitäten. Keine vollständigen Prompts oder Secrets speichern.
- Bei einer Änderung an Inhalten beide Dateien synchron aktualisieren.

## Qualität und Zuständigkeit

- Originale nicht stillschweigend modifizieren.
- Fehlende Belege oder widersprüchliche Quellen als Unsicherheit kennzeichnen.
- Wiki-Erkenntnisse niemals automatisch in normatives `doc/ai/PROJECT.md`, `ARCHITECTURE.md` oder ADRs übertragen.
- Keine vertraulichen oder urheberrechtlich geschützten Texte ohne Berechtigung committen.
- Der Validator kontrolliert Syntax, Verweise und lokale Quelldateien; semantische Wahrheit erfordert gesonderte Prüfung.
