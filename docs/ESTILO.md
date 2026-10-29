# Editor de la plantilla minimalista_onda

La configuración está en `estilos/minimalista_onda.json` y puede sobreescribirse para un caso usando `config.json > visual` o el comando `configurar visual.<clave> <valor>`.

| Clave | Uso |
|---|---|
| header_bg | Fondo hex RGB, por ejemplo ECECEC |
| header_radius | Radio de esquinas en puntos |
| header_pad | Separación interna de la cabecera |
| name / role / contact | Tamaños tipográficos del encabezado |
| photo_pt | Tamaño del retrato |
| wave_color | Gris del marco ondulado: C8CACC |
| wave_amplitude / wave_thickness | Ondulación y grosor del marco |
| icons / icon_color / icon_pt | Iconos lineales automáticos por categoría |
| divider_color / separator | Línea horizontal de sección o sin línea (`none`) |
| margin / body / title / section | Márgenes y tamaños de sección |
| block_gap / section_gap / leading | Densidad y separación |
| footer / repeat_name | Número de página y nombre en páginas siguientes |

Una edición puede provocar desbordamiento: repite `propuestas`, revisa las imágenes y no uses `cerrar` hasta inspeccionar ambos idiomas. Las fotografías se incorporan a los documentos individuales pero no al paquete distribuible. Los iconos se dibujan localmente, sin descargar recursos externos.

La edición de bloques (contenido, orden, sección, agrupación y eliminación) se realiza en `cv_es.json` y `cv_en.json` con confirmación del usuario; no se ejecuta un editor gráfico independiente. El flujo de Codex/Claude Code opera mediante conversación en VS Code.
