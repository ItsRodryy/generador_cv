"""Full integration tests; requires LibreOffice and Lato."""
import tempfile
import shutil
import unittest
import zipfile
from pathlib import Path
from generador_cv.modelo import ROOT,load,save
from generador_cv.cli import main
from generador_cv.pipeline import best
from generador_cv.importar import extract

DEMO=ROOT/'ejemplos'/'caso_ficticio'

class Integration(unittest.TestCase):
    def test_preview_and_complete_bilingual_flow(self):
        with tempfile.TemporaryDirectory() as t:
            case=Path(t)/'case';shutil.copytree(DEMO,case)
            for cmd in ('contenido','traduccion'):
                self.assertEqual(main(['aprobar',cmd,'--caso',str(case)]),0)
            self.assertEqual(main(['propuestas','--caso',str(case)]),0)
            self.assertEqual(main(['elegir','minimalista_onda','--caso',str(case)]),0)
            self.assertEqual(main(['generar','--caso',str(case)]),0)
            for lang in ('ES','EN'):
                for ext in ('docx','pdf'):
                    self.assertTrue((case/'salida'/f'CV_{lang}.{ext}').is_file())
            self.assertEqual(load(case/'salida'/'informe.json')['estado'],'PENDIENTE_REVISION_VISUAL')
            self.assertEqual(main(['cerrar','--caso',str(case),'--revisor','Revisión de prueba']),2)
            changed=load(case/'cv_en.json');changed['blocks'][0]['body'][0]+=' CAMBIO';save(case/'cv_en.json',changed)
            self.assertEqual(main(['generar','--caso',str(case)]),2)
    def test_three_pages_and_one_page_no_text_removed(self):
        with tempfile.TemporaryDirectory() as t:
            for pages in (1,3):
                cfg=load(DEMO/'config.json');cfg['paginas']=pages
                result=best(load(DEMO/'cv_es.json'),cfg,'minimalista_onda',Path(t)/str(pages),'CV_DEMO',DEMO)
                # The generator must not certify an impossible page count.
                self.assertTrue((Path(t)/str(pages)/'CV_DEMO.pdf').exists())
                if result['ok_tecnico']:
                    import fitz
                    self.assertEqual(len(fitz.open(Path(t)/str(pages)/'CV_DEMO.pdf')),pages)
    def test_pdf_import(self):
        with tempfile.TemporaryDirectory() as t:
            t=Path(t)
            src=t/'mini.pdf'
            import fitz
            p=fitz.open();x=p.new_page();x.insert_text((70,100),'Curriculum de persona ficticia');p.save(src)
            case=t/'private';case.mkdir()
            output=extract(src,case)
            self.assertIn('Curriculum',(output/'texto.txt').read_text())

if __name__=='__main__':unittest.main()
