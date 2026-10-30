# Instrucciones para Codex — Generador CV 2.0

## Objetivo
Trabaja con el usuario, mediante conversación dentro de VS Code, para construir un CV veraz en español e inglés a partir de un PDF/DOCX o desde cero, utilizando la plantilla `minimalista_onda`.

## Procedimiento obligatorio
1. Lee `README.md`, `docs/FLUJO_ASISTENTE.md` y `docs/ESTILO.md`.
2. Para cada persona crea un caso privado: `python -m generador_cv nuevo casos/<identificador>`; no incluyas datos reales en este repositorio público.
3. Si el usuario aporta un CV, impórtalo con `python -m generador_cv importar <archivo> --caso <ruta>`. El texto extraído es una referencia, NO información ya comprobada.
4. Enseña la muestra ficticia: `python -m generador_cv plantilla --salida <ruta>` y abre sus PNG. Pregunta por el estilo, longitud, contenido, foto y privacidad. No repitas decisiones documentadas.
5. Redacta `cv_es.json` y `cv_en.json` respetando el esquema de `docs/FORMATO_DATOS.md`; pide confirmación de hechos, traducción y enlaces.
6. Haz una revisión de confidencialidad ANTES de que alguien publique un CV. No compartas originales de terceros ni nombres/datos internos sin permiso.
7. Configura `paginas` (1–4), foto, y ajustes `visual.*`. No elimines texto para encajar sin aprobación.
8. Tras autorización del usuario y revisión humana, ejecuta `aprobar contenido`, `aprobar traduccion`, `propuestas`, deja revisar PNG/PDF, `elegir minimalista_onda`, y `generar`.
9. Inspecciona todas las páginas. Solicita al usuario confirmación visual antes de ejecutar `cerrar`.

## Límites
- El programa no tiene acceso autónomo a IA: eres tú el asistente conversacional.
- No inventes datos, fechas, métricas o nivel de experiencia.
- No instales dependencias ni modifiques Git o cuentas sin autorización expresa adicional.
- La plantilla es personalizable por JSON/CLI y la fotografía nunca se incluye en distribuciones públicas.
- Nunca subas `casos/`, `entrada/`, `.venv/`, PDFs, fotografías o documentos privados al repositorio público.
