---
name: knowledge-lint
description: Use when checking project-wiki structural integrity, provenance links, outdated claims and knowledge conflicts.
---

# Knowledge Lint

1. `knowledge/SCHEMA.md` lesen; prüfen, ob die optionale Wissensbasis aktiviert ist.
2. `just knowledge-validate` auf Metadaten, Quell-IDs, lokale Links und Indexverweise ausführen.
3. `just knowledge-stats` zur Erfassung der Seiten und Quellen verwenden.
4. Semantisch doppelte Aussagen, veraltete Belege, gegensätzliche Quellen und unbelegte Behauptungen gezielt überprüfen.
5. Eindeutige formale Fehler beheben; fachliche Streitfragen zur menschlichen Prüfung markieren.
6. Lint-Ergebnisse im `knowledge/wiki/log.md` datiert festhalten, wenn Inhalte korrigiert werden.

## Done when
- Formale Validierung erfolgreich oder Blocker mit genauen Pfaden dokumentiert.
- Semantische Risiken mit Quellenbezug benannt; keine fingierte Faktenprüfung.
