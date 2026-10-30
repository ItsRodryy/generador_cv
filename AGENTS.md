# Generador CV

Generador local de currículums ES/EN en DOCX y PDF, con plantilla minimalista_onda y revisión conversacional de Codex o Claude; no llama a proveedores de IA.

Autoría: Adrián Rodríguez Rodríguez (GitHub: ItsRodryy). Ninguna IA figura como autora ni firma nada.

## Forma de trabajar

- Responde en español, breve y directo. Durante el trabajo da un aviso breve cada 30–45 segundos, nunca más de 60 en silencio: qué has comprobado, qué haces y qué falta.
- Antes de una tarea mediana o grande, indica en una línea el modelo en uso y el esfuerzo que recomiendas.
- No expongas el enfoque salvo al planificar. Si una duda cambia el resultado, pregunta (cinco como
  máximo, juntas) y espera; después trabaja sin paradas salvo un bloqueo real. Sin dudas, actúa.
- El chat prevalece sobre estos documentos. Si el usuario decide algo nuevo o cambia algo escrito,
  actualiza el documento afectado en el mismo trabajo, sin esperar a que lo pida.
- Comprueba rutas y datos reales antes de usarlos; no inventes. Di lo que no hayas podido comprobar.
- Git: lee sin pedir permiso (`status`, `diff`, `log`, `show`, `blame`, `branch --list`, `remote -v`). Antes de cualquier operación que cambie algo (`add`, `commit`, `push`, `pull`, `fetch`, `checkout`, `switch`, `restore`, `reset`, `stash`, `merge`, `rebase`, `tag`, crear o borrar ramas, `config`, `init`, `clone`, `clean` o publicación), di exactamente qué vas a hacer, pide permiso y espera. El permiso vale solo para esa operación.
- Al terminar: qué se hizo, cómo se verificó y qué queda. Sin volcados de consola.

## Proyecto

- Plataformas: Windows 10/11, macOS/Linux (según README; sin verificar aquí).
- Tecnologías: Python 3.10+; python-docx; PyMuPDF; Pillow; LibreOffice o Word para PDF.
- No subir casos/, entrada/, .venv/, PDF, fotos ni documentos privados.
- Repositorio público: sin datos personales en ai_workspace.
- Antes de ayudar a crear un CV, leer contexto/asistente_cv.md; conserva el procedimiento completo anterior.
- No inventar datos, fechas, métricas ni experiencia; validar hechos y traducción con la persona.
- Una única plantilla inicial minimalista_onda; no resumir contenido para encajar ni publicar sin aprobación.
- El software no tiene acceso autónomo a IA; no instalar dependencias ni modificar cuentas sin orden expresa.
- Intocable sin orden expresa: casos/, entrada/, .venv/, PDF, fotos y documentos privados: no subirlos; Repositorio público: sin datos personales en ai_workspace.

## Verificación

Proporcional al riesgo: en cambios pequeños, solo lo afectado; todo en cambios grandes y al cerrar.

- `python -m unittest discover -s tests -p 'test_*.py' -v`
- `python -m unittest discover -s tests -p 'integration.py' -v (requiere LibreOffice/Word y Lato)`

## Estado, planes y memoria

- Estado: `ai_workspace/ESTADO.md`. Si existe `PLAN_ACTUAL.md`, léelo antes de retomar.
- Skills: `crear-plan` planifica y para; `ejecutar-plan` ejecuta (la orden aprueba el plan);
  `cerrar` verifica, compacta y archiva, o deja el traspaso si solo se pausa; `error` diagnostica;
  `progreso` (= `estado`) retoma y da el avance (`ai_workspace/progreso.md`). Mensajes: según
  `ai_workspace/contexto/personas.md`; nada está enviado sin confirmarlo el usuario.
- `ai_workspace/` guarda solo documentos breves y vigentes: ni copias de código, ni binarios, ni
  informes viejos, ni traspasos duplicados. Los temporales van fuera del proyecto. Los límites de
  tamaño están en `ai_workspace/configuracion.json`.
- Graphify: antes de abrir archivos grandes, `graphify explain <símbolo>` o `graphify affected <símbolo>`. `cerrar` lo actualiza.

## Documentación bajo demanda

Rutas dentro de `ai_workspace/`.

| Si vas a… | Lee |
|---|---|
| ayudar a una persona a crear su CV | `contexto/asistente_cv.md` |
| consultar las instrucciones originales de Claude para el CV | `contexto/asistente_claude.md` |
