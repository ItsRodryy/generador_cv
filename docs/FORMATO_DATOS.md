# Modelo de datos JSON

`cv_es.json` y `cv_en.json` contienen la misma identidad, contactos y bloques con IDs idénticos, para proteger la paridad entre idiomas.

```json
{
  "language": "es",
  "person": {
    "name": "Alex Ejemplo",
    "headline": "Desarrollador software",
    "contacts": ["Ciudad Ejemplo", "alex@example.com", "https://example.com"]
  },
  "blocks": [
    {
      "id": "profile", "section": "Perfil profesional", "title": "Perfil",
      "meta": "", "category": "profile", "body": ["Texto comprobado."],
      "bullets": [], "links": [], "protected": []
    }
  ]
}
```

Cada bloque tiene `id`, `section` (dejar vacío en las entradas continuas), `title`, `meta`, `body`, `bullets`, `links`, `category` (profile / experience / skills / project / education / language / other), `protected` (hechos literales que deben figurar en ambos idiomas), y `auxiliary` (obsoleto pero permitido). El asistente debe conservar los hechos, no traducir o reformatear arbitrariamente fechas y niveles de `protected`, y pedir permiso para cambios sustantivos. Los bloques se mantienen indivisibles por diseño. Los enlaces admiten solo http(s) y mailto. Se recomienda mantener `blocks` en el mismo orden para las dos versiones.
