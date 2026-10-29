import copy
import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from PIL import Image
from docx import Document
from generador_cv.modelo import ROOT,load,save,check,bilingual,digest
from generador_cv.pipeline import _possible_cuts,generate,STYLES
from generador_cv.componer import compose,style
from generador_cv.cli import main
from generador_cv.importar import extract
from generador_cv.recursos import wavy_photo
from generador_cv.seguridad import warnings

DEMO=ROOT/'ejemplos'/'caso_ficticio'

class Core(unittest.TestCase):
    def test_one_template_only(self):
        self.assertEqual(STYLES,['minimalista_onda'])
        self.assertEqual(style('minimalista_onda')['wave_color'],'C8CACC')
        with self.assertRaises(ValueError):style('europass')
    def test_bilingual_structure(self):
        self.assertEqual(bilingual(load(DEMO/'cv_es.json'),load(DEMO/'cv_en.json')),[])
    def test_facts_and_duplicates(self):
        data=load(DEMO/'cv_es.json');data['blocks'].append(data['blocks'][0]);
        with self.assertRaises(ValueError):check(data)
        es,en=load(DEMO/'cv_es.json'),load(DEMO/'cv_en.json');en['blocks'][1]['bullets'][0]='Worked with data.'
        self.assertTrue(any('Python' in e for e in bilingual(es,en)))
    def test_validation_and_size(self):
        with tempfile.TemporaryDirectory() as t:
            d=Path(t)/'caso';self.assertEqual(main(['nuevo',str(d)]),0)
            self.assertEqual(main(['configurar','--caso',str(d),'paginas','3']),0)
            self.assertEqual(load(d/'config.json')['paginas'],3)
            self.assertEqual(main(['configurar','--caso',str(d),'paginas','5']),2)
            self.assertEqual(main(['configurar','--caso',str(d),'visual.wave_color','C9CBCD']),0)
            self.assertEqual(load(d/'config.json')['visual']['wave_color'],'C9CBCD')
    def test_page_combinations(self):
        blocks=load(DEMO/'cv_es.json')['blocks']
        self.assertEqual(_possible_cuts(blocks,1),[None])
        self.assertTrue(all(len(c)==2 for c in _possible_cuts(blocks,3)))
        with self.assertRaises(ValueError):_possible_cuts(blocks,5)
    def test_import_preserves_original(self):
        with tempfile.TemporaryDirectory() as t:
            t=Path(t);src=t/'original.docx';case=t/'case';case.mkdir()
            compose(load(DEMO/'cv_es.json'),load(DEMO/'config.json'),'minimalista_onda',src,(3,),DEMO)
            original=src.read_bytes()
            output=extract(src,case)
            self.assertIn('Alex Ejemplo',(output/'texto.txt').read_text())
            self.assertEqual((case/'originales'/'original.docx').read_bytes(),original)
            with self.assertRaises(ValueError):extract(src,case)
    def test_photo_undistorted(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'photo.png'
            wavy_photo(DEMO/'retrato_ficticio.png',p,style())
            with Image.open(p) as im:self.assertEqual(im.size,(450,450))
            d=Path(t)/'test.docx'
            compose(load(DEMO/'cv_es.json'),load(DEMO/'config.json'),'minimalista_onda',d,(3,),DEMO)
            doc=Document(d)
            self.assertTrue(doc.inline_shapes)
            with zipfile.ZipFile(d) as z:
                raw=z.read('word/document.xml')
                self.assertIn(b'Alex Ejemplo',raw)
                self.assertNotIn(b'CURRICULUM',raw)
    def test_confidentiality_warnings(self):
        src=load(DEMO/'cv_es.json')
        src['blocks'][0]['body'].append('Servidor 192.168.1.12')
        self.assertTrue(warnings(src))
    def test_no_final_without_approval(self):
        with self.assertRaises(ValueError):generate(DEMO)

if __name__=='__main__':unittest.main()
