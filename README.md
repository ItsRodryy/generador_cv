# Generador CV 2.0 · Minimalista Onda

Generador **local** de currículums en español e inglés, con una única plantilla inicial: cabecera gris de esquinas suaves, fotografía circular con borde ondulado gris claro, iconos lineales discretos, separadores horizontales y diseño de una columna. Produce **DOCX editable y PDF** a partir de datos estructurados. La conversación, traducción, decisiones y revisión visual se realizan con **Codex o Claude Code en VS Code**; el programa NO llama a ningún proveedor de IA ni necesita claves API.

## Inicio rápido (Windows 10/11)

1. Descomprime el ZIP en una carpeta NUEVA y ábrela en VS Code. Conserva tus casos privados por separado; no los borres al sustituir versiones.
2. Instala por tu cuenta Python 3.10+ y LibreOffice, y utiliza un entorno propio. Este programa no instala dependencias automáticamente.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m generador_cv doctor
.\.venv\Scripts\python.exe -m generador_cv plantilla --salida vista_demo
```

Para macOS/Linux: `python3 -m venv .venv`, `source .venv/bin/activate`, `python -m pip install -e .` y `python -m generador_cv doctor`.

3. Abre `AGENTS.md` con Codex o `CLAUDE.md` con Claude Code. Indica qué CV PDF/DOCX quieres adaptar y pide que te haga las preguntas del flujo. El asistente abrirá los PNG generados y te preguntará qué cambiar.

## Flujo manual

```sh
python -m generador_cv nuevo casos/demostracion
python -m generador_cv importar /ruta/ejemplo.pdf --caso casos/demostracion
python -m generador_cv preguntas --caso casos/demostracion
# Aquí el asistente redacta cv_es.json y cv_en.json y pide revisión.
python -m generador_cv configurar --caso casos/demostracion paginas 2
python -m generador_cv configurar --caso casos/demostracion visual.wave_color C8CACC
python -m generador_cv visual --caso casos/demostracion
python -m generador_cv confidencialidad --caso casos/demostracion
# Tras confirmar los textos:
python -m generador_cv aprobar contenido --caso casos/demostracion
python -m generador_cv aprobar traduccion --caso casos/demostracion
python -m generador_cv propuestas --caso casos/demostracion
# Abre casos/demostracion/propuestas/minimalista_onda/CV_ES_paginas/*.png
python -m generador_cv elegir minimalista_onda --caso casos/demostracion
python -m generador_cv generar --caso casos/demostracion
# Tras inspección visual real de ambos PDF:
python -m generador_cv cerrar --caso casos/demostracion --revisor "Usuario" --confirmo-inspeccion-visual
```

Generar PDF requiere LibreOffice o Microsoft Word (Windows). Indica `CV_SOFFICE` si el ejecutable está fuera de las ubicaciones detectadas. El archivo `ejemplos/caso_ficticio` es totalmente ficticio; su fotografía es una ilustración geométrica, NO de una persona real.

## Qué se puede modificar

La única plantilla editable es `estilos/minimalista_onda.json`, cuyos parámetros se aplican desde `config.json` (`visual`) o mediante `configurar visual.<parámetro> <valor>`. Se pueden ajustar márgenes, fuentes y tamaños, proporciones, fondo, radio de cabecera, foto, intensidad y color de la onda, iconos, espaciados y separadores. La sección se puede ocultar, renombrar o reordenar editando los `blocks` bajo supervisión del asistente. Detalles: `docs/ESTILO.md`.

El número de páginas se elige de **1 a 4**, sin rellenar ni resumir automáticamente. Si no cabe, se bloquea y pide revisión. Los PDF se generan del mismo DOCX nativo. Los enlaces son clicables; el texto es editable en Word. La paginación puede variar según sistema, fuente y versión de Word: revisa el PDF en el equipo final.

## Privacidad y publicación

**No publiques el ZIP original que incluía `.venv`, documentos personales y salidas reales.** Esta distribución solo contiene código, documentación, pruebas y un ejemplo ficticio; no incluye tu fotografía ni CV. `.gitignore` excluye `casos/` y `entrada/`, pero **no limpia archivos que ya hayan sido añadidos a Git**. Inspecciona `git status`, cada archivo y el historial antes de publicar. El detector de confidencialidad es orientativo y no sustituye aprobación de la empresa ni asesoría legal.

## Pruebas

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
python -m unittest discover -s tests -p 'integration.py' -v
python -m generador_cv plantilla --salida vista_demo
```

Las pruebas de integración requieren LibreOffice/Word y una instalación local de Lato. **No redistribuimos archivos de fuentes.** Licencia del proyecto: **MIT** (consulta `LICENSE`). Las fuentes tipográficas y las herramientas de terceros mantienen sus propias licencias.
