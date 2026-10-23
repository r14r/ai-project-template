---
name: knowledge-query
description: Use when answering project domain questions from a curated Markdown wiki and its cited original sources.
---

# Knowledge Query

1. Zweck und Grenzen aus `AGENTS.md` und `doc/ai/CONTEXT.md` einordnen.
2. Zuerst `knowledge/wiki/index.md` lesen; nur einschlägige Wiki-Seiten öffnen.
3. Für entscheidende Aussagen die in Frontmatter und Fließtext genannten Originalquellen kontrollieren.
4. Bei fehlendem Kontext gezielt nachprüfen; bei Konflikten Standpunkte und Unsicherheit benennen.
5. Antwort mit nachvollziehbaren Quellenangaben und klarer Trennung von Fakt und Schlussfolgerung liefern.
6. Neue, belastbare Erkenntnisse nur bei Bedarf und mit `knowledge-ingest`-Regeln persistieren, nicht automatisch jedes Chatgespräch speichern.

## Done when
- Relevante Aussagen belegbar, Quellenkonflikte transparent und die verwendeten Quellen bezeichnet.
- Fehlender Zugriff auf Quellen ist ausdrücklich vermerkt.
