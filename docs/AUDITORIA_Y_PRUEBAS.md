# Cobertura y validación del generador v2

Se parte del código del ZIP de octubre de 2026, conservando importación PDF/DOCX, representación JSON bilingüe, exportación con LibreOffice o Word y validación de hechos protegidos. Se reemplazan los cinco estilos por una plantilla única, configurada con fotos de onda y cabecera de cuatro esquinas suaves, y se habilita la extensión de 1–4 páginas.

Las pruebas unitarias cubren modelo bilingüe, no duplicación de IDs, modificación de configuración, validación de diseño, importación de originales y escaneo orientativo de confidencialidad. La integración cubre ambos idiomas, exportación PDF/Word y regeneración después de una modificación.

Ninguna validación automática certifica igual render en todas las versiones de Word, compatibilidad ATS ni permisos de confidencialidad. Es obligatoria la inspección visual de todas las páginas y la aprobación humana antes de publicar los CV.
