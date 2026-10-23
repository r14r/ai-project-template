---
name: knowledge-ingest
description: Use when adding or revising authoritative source material and deriving traceable project-knowledge wiki entries.
---

# Knowledge Ingest

1. `AGENTS.md`, `doc/ai/CONTEXT.md`, `knowledge/SCHEMA.md` und `knowledge/wiki/index.md` lesen.
2. Berechtigung und Vertraulichkeit der Rohquelle sowie den bestehenden Manifest-Eintrag prüfen.
3. Originaldatei nicht verändern; externe Quelle über URI und bei Bedarf Hash inventarisieren.
4. Bestehende Wiki-Seiten recherchieren, um Duplikate und widersprüchliche Behauptungen zu erkennen.
5. Fachliche Aussagen vorsichtig synthetisieren; jede wichtige Behauptung mit einer realen Quellen-ID belegen.
6. Seiten mit gültigem Frontmatter erstellen/aktualisieren; Widersprüche mit Status `disputed` markieren.
7. Wiki-Index und datiertes Log ergänzen.
8. `just knowledge-validate` ausführen und formale Fehler beseitigen.

Keine automatische Änderung von Anforderungen, ADRs oder Sicherheitsregeln. Keine vertraulichen Rohdokumente ohne explizite Freigabe committen.

## Done when
- Quelleninventar und Wiki-Seiten konsistent, nachvollziehbar und syntaktisch valide.
- Offene Unsicherheiten kenntlich und Prüfstatus berichtet.
