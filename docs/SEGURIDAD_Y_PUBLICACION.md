# Revisión previa a publicación

- Usar **solo** el paquete limpio. El ZIP original incluía datos personales, fotografía, PDF privados, `.venv` y resultados de trabajo: NO copiar esas carpetas al repositorio público.
- El árbol distribuible no incluye `casos/`, `entrada/`, `.venv`, exportaciones, imágenes personales, ni versiones de CV reales. El ejemplo incluido es ficticio y utiliza un retrato geométrico.
- Antes de `git add`, inspeccionar nombres de archivo, `git status` y diffs. `.gitignore` no protege elementos incluidos en commits anteriores.
- No subir credenciales, tokens, IPs, rutas privadas, datos de clientes, modelos comerciales ni código propietario.
- No tratar al asistente de IA como validador jurídico: su detección de datos sensibles puede fallar.
- El propietario deberá decidir una licencia antes de permitir reutilización pública del código. No se incluye licencia por defecto.
- No se modifica Git desde este paquete. Las operaciones remotas y la publicación se realizan exclusivamente cuando se autoricen expresamente.
