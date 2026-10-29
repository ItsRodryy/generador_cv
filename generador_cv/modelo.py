import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(case):
    h = hashlib.sha256()
    for name in ["cv_es.json", "cv_en.json", "config.json"]:
        p = case / name
        h.update(name.encode())
        h.update(p.read_bytes() if p.exists() else b"MISSING")
    config = load(case / "config.json")
    for p in sorted((case / "originales").glob("*")):
        if p.is_file():
            h.update(p.name.encode())
            h.update(p.read_bytes())
    for key in ["foto"]:
        if config.get(key):
            h.update((case / config[key]).read_bytes())
    return h.hexdigest()


def norm(s):
    import unicodedata
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s)).casefold()


def block_text(b):
    return [str(b.get(k, "")) for k in ("section", "title", "meta")] + b.get("body", []) + b.get("bullets", []) + [x["label"] for x in b.get("links", [])]


def check(data):
    if not isinstance(data, dict) or data.get("language") not in ("es", "en"):
        raise ValueError("language debe ser es o en")
    if not data.get("person", {}).get("name") or not data.get("blocks"):
        raise ValueError("Falta person.name o blocks")
    ids = []
    for b in data["blocks"]:
        if not b.get("id") or not b.get("title"):
            raise ValueError("Cada bloque necesita id y title")
        ids.append(b["id"])
        for key in ["body", "bullets", "protected"]:
            if not isinstance(b.get(key, []), list) or any(not isinstance(s, str) for s in b.get(key, [])):
                raise ValueError(f"{b['id']}.{key} debe ser una lista de textos")
        for link in b.get("links", []):
            if not link.get("label") or not re.match(r"^(https?://|mailto:)", link.get("url", "")):
                raise ValueError("Enlace inválido; solo http, https o mailto")
    if len(ids) != len(set(ids)):
        raise ValueError("IDs de bloque duplicados")


def bilingual(es, en):
    check(es)
    check(en)
    errors = []
    if es["language"] != "es" or en["language"] != "en":
        errors.append("Idiomas de los archivos intercambiados")
    if es["person"].get("name") != en["person"].get("name") or es["person"].get("contacts", []) != en["person"].get("contacts", []):
        errors.append("Datos personales distintos entre idiomas")
    if [b["id"] for b in es["blocks"]] != [b["id"] for b in en["blocks"]]:
        errors.append("Bloques u orden distintos entre idiomas")
    for a, b in zip(es["blocks"], en["blocks"]):
        if a.get("protected", []) != b.get("protected", []):
            errors.append(f"Hechos protegidos distintos: {a['id']}")
        for value in a.get("protected", []):
            if norm(value) not in norm(" ".join(block_text(a))) or norm(value) not in norm(" ".join(block_text(b))):
                errors.append(f"Hecho protegido ausente: {a['id']}: {value}")
        if a.get("links", []) != b.get("links", []):
            # La etiqueta se puede traducir; el destino no cambia.
            if [l['url'] for l in a.get('links', [])] != [l['url'] for l in b.get('links', [])]:
                errors.append(f"Enlaces distintos: {a['id']}")
    return errors


def initial_config():
    return {"paginas": 2, "fuente": "Lato", "foto": None,
            "foto_confirmada": False, "estilo": "minimalista_onda", "visual": {}}
