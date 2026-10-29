"""Extracción conservadora: nunca confunde texto bruto con un CV revisado."""
import hashlib
import shutil
import zipfile
from pathlib import Path
import fitz
from docx import Document
from .modelo import save


def extract(source, case):
    source, case = Path(source).resolve(), Path(case).resolve()
    if source.suffix.lower() not in (".pdf", ".docx"):
        raise ValueError("Solo PDF y DOCX. No se ejecutan macros ni instrucciones del documento.")
    dest = case / "originales" / source.name
    if dest.exists():
        raise ValueError("Ya existe ese original; usa otro nombre o un caso nuevo")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
    out = case / "extraccion" / source.stem
    out.mkdir(parents=True, exist_ok=False)
    report = {"original": str(dest.relative_to(case)), "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
              "advertencias": [], "fuentes": [], "imagenes": []}
    text = []
    if source.suffix.lower() == ".pdf":
        with fitz.open(dest) as doc:
            for i, page in enumerate(doc, 1):
                text.append(f"\n--- PÁGINA {i} ---\n" + page.get_text(sort=True))
                page.get_pixmap(matrix=fitz.Matrix(1.25, 1.25)).save(out / f"pagina-{i}.png")
                report["fuentes"].extend(s["font"] for b in page.get_text("dict")["blocks"] if b["type"] == 0 for l in b["lines"] for s in l["spans"])
                if len(page.get_text().strip()) < 25:
                    report["advertencias"].append(f"Página {i}: poco texto; revisar escaneo y solicitar OCR local. No se ha aplicado OCR.")
                for j, img in enumerate(page.get_images(full=True)):
                    obj = doc.extract_image(img[0])
                    filename = f"imagen-{i}-{j}.{obj['ext']}"
                    (out / filename).write_bytes(obj["image"])
                    report["imagenes"].append(filename)
        report["fuentes"] = sorted(set(report["fuentes"]))
    else:
        doc = Document(dest)
        from docx.oxml.ns import qn
        # Orden del cuerpo, incluidos párrafos de tablas anidadas; cada párrafo una vez.
        for p in doc.element.body.iter(qn("w:p")):
            text.append("".join(t.text or "" for t in p.iter(qn("w:t"))))
        report["advertencias"].append("DOCX: revisar también cabeceras, pies y cuadros de texto; la extracción del cuerpo no conserva la composición visual.")
        report["fuentes"] = sorted(set(r.font.name for p in doc.paragraphs for r in p.runs if r.font.name))
        with zipfile.ZipFile(dest) as z:
            for name in z.namelist():
                if name.startswith("word/media/") and not name.endswith("/"):
                    filename = Path(name).name
                    (out / filename).write_bytes(z.read(name))
                    report["imagenes"].append(filename)
    (out / "texto.txt").write_text("\n".join(text), encoding="utf-8")
    save(out / "informe.json", report)
    return out
