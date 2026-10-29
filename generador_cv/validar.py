"""Comprobaciones técnicas; nunca sustituyen una inspección visual humana/IA."""
import re
from pathlib import Path
import fitz
from .modelo import norm, block_text


def link_normal(value):
    from urllib.parse import urlsplit, urlunsplit
    p = urlsplit(value)
    if p.scheme in ("http", "https"):
        return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path or "/", p.query, p.fragment))
    return value


def validate(pdf_path, data, config, docx_path=None):
    errors, warnings, details = [], [], []
    with fitz.open(pdf_path) as doc:
        texts = [norm(p.get_text()) for p in doc]
        if len(doc) != config["paginas"]:
            errors.append(f"Se esperaban {config['paginas']} páginas y hay {len(doc)}")
        for b in data["blocks"]:
            fragments = [norm(t) for t in block_text(b) if t.strip()]
            pages = [i + 1 for i, text in enumerate(texts) if all(f in text for f in fragments)]
            if not pages:
                errors.append(f"Bloque ausente, dividido o texto alterado: {b['id']}")
            details.append({"bloque": b["id"], "paginas": pages})
        alltext = "".join(texts)
        for value in [data["person"]["name"], data["person"].get("headline", ""), *data["person"].get("contacts", [])]:
            if value and norm(value) not in alltext:
                errors.append("Dato de cabecera ausente: " + value)
        used, ink, families, links = [], [], set(), set()
        for i, p in enumerate(doc, 1):
            page_spans, lines = [], []
            for b in p.get_text("dict")["blocks"]:
                if b["type"] != 0:
                    continue
                for line in b["lines"]:
                    spans = [s for s in line["spans"] if s["text"].strip()]
                    page_spans.extend(spans)
                    if spans and not (line["bbox"][1] > p.rect.height * .9 and "".join(s["text"] for s in spans).strip().isdigit()):
                        lines.append(fitz.Rect(line["bbox"]))
            for s in page_spans:
                r = fitz.Rect(s["bbox"])
                families.add(s["font"])
                if not p.rect.contains(r):
                    errors.append(f"Página {i}: texto fuera del A4")
                if s["size"] < 8.8:
                    errors.append(f"Página {i}: texto menor de 8,8 pt")
                if '\ufffd' in s['text']:
                    errors.append(f"Página {i}: carácter de sustitución")
            for j, a in enumerate(lines):
                for b in lines[j+1:]:
                    intersection = a & b
                    if not intersection.is_empty and intersection.width > 4 and intersection.height > min(a.height, b.height) * .55:
                        errors.append(f"Página {i}: posible solapamiento de texto")
            ink.append(sum(r.get_area() for r in lines))
            used.append(max((r.y1 for r in lines), default=0) - min((r.y0 for r in lines), default=0))
            links.update(l.get("uri", "") for l in p.get_links())
            if abs(p.rect.width - 595.28) > 2 or abs(p.rect.height - 841.89) > 2:
                errors.append(f"Página {i}: formato distinto de A4")
            for image in p.get_image_info():
                r = fitz.Rect(image["bbox"])
                if not p.rect.contains(r):
                    errors.append(f"Página {i}: imagen fuera de página")
                if any((r & t).get_area() > t.get_area() * .15 for t in lines):
                    errors.append(f"Página {i}: imagen sobre texto")
        wanted = re.sub(r"[^a-z]", "", config["fuente"].lower())
        if not families or any(wanted not in re.sub(r"[^a-z]", "", f.lower()) for f in families):
            errors.append("Posible sustitución tipográfica; esperada " + config["fuente"] + "; PDF: " + ", ".join(sorted(families)))
        expected = {l["url"] for b in data["blocks"] for l in b.get("links", [])}
        expected.update(x if x.startswith(("http://", "https://", "mailto:")) else 'mailto:' + x for x in data['person'].get('contacts', []) if x.startswith(('http://', 'https://', 'mailto:')) or ('@' in x and ' ' not in x))
        for link in {link_normal(v) for v in expected} - {link_normal(v) for v in links}:
            errors.append("Enlace no conservado: " + link)
        ratio = min(used) / max(used) if used and max(used) else 0
        ink_ratio = min(ink) / max(ink) if ink and max(ink) else 0
        score = .6 * ink_ratio + .4 * ratio
        if ratio < .45:
            errors.append("Distribución desequilibrada entre páginas")
        if used and max(used) < 350:
            warnings.append("Contenido breve para el número de páginas; revisar espacios sin añadir relleno")
        if config.get("foto") and not any(p.get_image_info() for p in doc):
            errors.append("Falta la fotografía en PDF")
        for i, p in enumerate(doc):
            if not p.get_text().strip():
                errors.append(f"Página {i+1} vacía")
    if docx_path:
        from docx import Document
        from PIL import Image
        import zipfile, io
        d = Document(docx_path)
        if config.get("foto") and not d.inline_shapes:
            errors.append("Falta foto en DOCX")
        with zipfile.ZipFile(docx_path) as z:
            xml = z.read("word/document.xml")
            if b'w:txbxContent' in xml:
                errors.append("Hay cuadros de texto: revisar orden de lectura")
        for shape in d.inline_shapes:
            rid = shape._inline.graphic.graphicData.pic.blipFill.blip.embed
            with Image.open(io.BytesIO(d.part.related_parts[rid].blob)) as im:
                if abs((shape.width/shape.height)/(im.width/im.height)-1) > .02:
                    errors.append("Fotografía deformada en Word")
    warnings.append("Revisión visual pendiente: recortes, huecos, jerarquía, foto y lectura. No se certifican automáticamente.")
    return {"ok_tecnico": not errors, "errores": sorted(set(errors)), "avisos": warnings,
            "bloques": details, "ocupacion_pt": used, "equilibrio": round(ratio, 3), "equilibrio_tinta": round(ink_ratio, 3), "puntuacion": round(score, 3), "fuentes_pdf": sorted(families)}


def render(pdf, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with fitz.open(pdf) as d:
        for i, p in enumerate(d, 1):
            p.get_pixmap(matrix=fitz.Matrix(1.5, 1.5)).save(directory / f"pagina-{i}.png")
