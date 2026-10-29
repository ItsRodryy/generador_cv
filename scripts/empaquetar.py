"""Create a reproducible public package using a positive allowlist (never private cases)."""
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KEEP = [
    '.gitignore','AGENTS.md','CLAUDE.md','README.md','pyproject.toml',
    'docs/AUDITORIA_Y_PRUEBAS.md','docs/ESTILO.md','docs/FLUJO_ASISTENTE.md',
    'docs/FORMATO_DATOS.md','docs/SEGURIDAD_Y_PUBLICACION.md',
    'estilos/minimalista_onda.json',
    'generador_cv/__init__.py','generador_cv/__main__.py','generador_cv/cli.py',
    'generador_cv/componer.py','generador_cv/exportar.py','generador_cv/importar.py',
    'generador_cv/modelo.py','generador_cv/pipeline.py','generador_cv/recursos.py',
    'generador_cv/seguridad.py','generador_cv/validar.py',
    'tests/test_core.py','tests/integration.py',
    'ejemplos/caso_ficticio/PREGUNTAS_Y_DECISIONES.md','ejemplos/caso_ficticio/config.json',
    'ejemplos/caso_ficticio/cv_es.json','ejemplos/caso_ficticio/cv_en.json',
    'ejemplos/caso_ficticio/estado.json','ejemplos/caso_ficticio/retrato_ficticio.png',
    'ejemplos/vista_previa/CV_DEMO.docx','ejemplos/vista_previa/CV_DEMO.pdf',
    'scripts/empaquetar.py'
]

def main():
    target=ROOT.parent/'generador_cv_v2_publicable.zip'
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name in KEEP:
            path=ROOT/name
            if not path.is_file():raise RuntimeError('Falta un archivo requerido: '+name)
            archive.write(path, 'generador_cv/'+name)
    print('ZIP:',target,'archivos:',len(KEEP),'tamaño:',target.stat().st_size)
if __name__=='__main__':main()
