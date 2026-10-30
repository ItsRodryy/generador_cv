# Graph Report - generador_cv  (2026-10-30)

## Corpus Check
- 53 files · ~10,946 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 152 nodes · 279 edges · 36 communities (23 shown, 13 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `105b9478`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- cli.py
- componer.py
- load
- Progreso del proyecto
- block_text
- planes.ps1
- Generador CV
- Generador CV 2.0 · Minimalista Onda
- Instrucciones para Codex — Generador CV 2.0
- Estado
- empaquetar.py
- CHANGELOG.md
- asistente_claude.md
- personas.md
- registro_trabajo.md
- AUDITORIA_Y_PRUEBAS.md
- ESTILO.md
- FLUJO_ASISTENTE.md
- FORMATO_DATOS.md
- SEGURIDAD_Y_PUBLICACION.md
- PREGUNTAS_Y_DECISIONES.md
- __init__.py
- generador-cv

## God Nodes (most connected - your core abstractions)
1. `load()` - 20 edges
2. `main()` - 19 edges
3. `best()` - 15 edges
4. `compose()` - 12 edges
5. `save()` - 12 edges
6. `bilingual()` - 11 edges
7. `style()` - 10 edges
8. `generate()` - 10 edges
9. `Core` - 10 edges
10. `_header()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `style()`  [EXTRACTED]
  generador_cv/cli.py → generador_cv/componer.py
- `main()` --calls--> `load()`  [EXTRACTED]
  generador_cv/cli.py → generador_cv/modelo.py
- `main()` --calls--> `warnings()`  [EXTRACTED]
  generador_cv/cli.py → generador_cv/seguridad.py
- `best()` --calls--> `style()`  [EXTRACTED]
  generador_cv/pipeline.py → generador_cv/componer.py
- `best()` --calls--> `compose()`  [EXTRACTED]
  generador_cv/pipeline.py → generador_cv/componer.py

## Import Cycles
- None detected.

## Communities (36 total, 13 thin omitted)

### Community 0 - "cli.py"
Cohesion: 0.27
Nodes (18): main(), Local CLI; AI interview is performed in VS Code by Codex/Claude after user…, convert(), office(), extract(), Extracción conservadora: nunca confunde texto bruto con un CV revisado., bilingual(), check() (+10 more)

### Community 1 - "componer.py"
Cohesion: 0.21
Nodes (19): _block(), _cell_margin(), compose(), _header(), _link(), _para(), Native editable Word with one configurable Minimalista Onda template., _rgb() (+11 more)

### Community 2 - "load"
Cohesion: 0.20
Nodes (4): style(), load(), Integration, Core

### Community 3 - "Progreso del proyecto"
Cohesion: 0.22
Nodes (8): Ahora, En marcha, Esperando a otros, Funciona y falla, Lo pedido, Mensajes, Progreso del proyecto, Proyecto

### Community 4 - "block_text"
Cohesion: 0.33
Nodes (7): block_text(), norm(), Conservative, non-blocking publication warnings. NOT a confidentiality…, warnings(), link_normal(), Comprobaciones técnicas; nunca sustituyen una inspección visual humana/IA., validate()

### Community 5 - "planes.ps1"
Cohesion: 0.32
Nodes (3): Leer-Plan(), Medir(), Obtener-Limites()

### Community 6 - "Generador CV"
Cohesion: 0.29
Nodes (6): Documentación bajo demanda, Estado, planes y memoria, Forma de trabajar, Generador CV, Proyecto, Verificación

### Community 7 - "Generador CV 2.0 · Minimalista Onda"
Cohesion: 0.29
Nodes (6): Flujo manual, Generador CV 2.0 · Minimalista Onda, Inicio rápido (Windows 10/11), Privacidad y publicación, Pruebas, Qué se puede modificar

### Community 8 - "Instrucciones para Codex — Generador CV 2.0"
Cohesion: 0.40
Nodes (4): Instrucciones para Codex — Generador CV 2.0, Límites, Objetivo, Procedimiento obligatorio

### Community 9 - "Estado"
Cohesion: 0.40
Nodes (4): Estado, Hecho y verificado, Por confirmar, Siguiente paso

## Knowledge Gaps
- **34 isolated node(s):** `generador-cv`, `Forma de trabajar`, `Proyecto`, `Verificación`, `Estado, planes y memoria` (+29 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load()` connect `load` to `cli.py`, `componer.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Why does `compose()` connect `componer.py` to `cli.py`, `load`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `main()` connect `cli.py` to `load`, `block_text`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **What connects `generador-cv`, `Forma de trabajar`, `Proyecto` to the rest of the system?**
  _34 weakly-connected nodes found - possible documentation gaps or missing edges._