"""Reproducible layout search, approval gate and ES/EN export."""
from itertools import combinations
from pathlib import Path
import shutil
import tempfile
from .modelo import load, save, check, bilingual, digest, block_text
from .componer import compose, style, DEFAULT_STYLE
from .exportar import convert
from .validar import validate, render

STYLES=[DEFAULT_STYLE]

def _possible_cuts(blocks,pages):
    n=len(blocks)
    if pages==1:return [None]
    if pages>n:raise ValueError('No puede haber más páginas que bloques. Revisar la estructura antes de generar.')
    if pages>4:raise ValueError('Se admiten de 1 a 4 páginas A4 en esta versión.')
    cuts=list(combinations(range(1,n),pages-1))
    if len(cuts)<=24:return cuts
    # Rank page boundaries by approximated text density; actual rendering remains authoritative.
    weights=[max(15,sum(len(x) for x in block_text(b))+40) for b in blocks]
    cum=[0]
    for w in weights:cum.append(cum[-1]+w)
    total=cum[-1]
    def penalty(indices):
        ticks=(0,*indices,n)
        sizes=[cum[b]-cum[a] for a,b in zip(ticks,ticks[1:])]
        return sum(((size-total/pages)/total)**2 for size in sizes)
    return sorted(cuts,key=penalty)[:24]

def best(data,config,name,dest,stem,case):
    check(data);pages=config.get('paginas',2)
    if isinstance(pages,bool) or not isinstance(pages,int) or pages<1 or pages>4:raise ValueError('paginas debe ser un entero entre 1 y 4')
    if config.get('foto') and not config.get('foto_confirmada'):raise ValueError('Fotografía sin confirmar')
    if not config.get('fuente'):raise ValueError('Elige fuente antes de generar (p. ej. Lato)')
    s=style(name,config.get('visual'))
    cuts=_possible_cuts(data['blocks'],pages)
    dest=Path(dest);dest.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cv-layout-') as scratch:
        temp=Path(scratch);docs=[]
        for i,cut in enumerate(cuts):
            path=temp/f'candidato-{i}.docx'
            compose(data,config,name,path,cut,case)
            docs.append(path)
        pdfs=convert(docs,temp/'pdf')
        results=[validate(p,data,config,dx) for p,dx in zip(pdfs,docs)]
        valid=[i for i,r in enumerate(results) if r['ok_tecnico']]
        chosen=max(valid,key=lambda i:results[i]['puntuacion']) if valid else min(range(len(results)),key=lambda i:len(results[i]['errores']))
        report=results[chosen]
        report.update(estilo=name,corte=cuts[chosen],candidatos=len(cuts),estado='PENDIENTE_REVISION_VISUAL' if valid else 'BLOQUEADO')
        if not valid:report['propuesta']='Contenido no cabe o hay errores: revisar la maqueta y solicitar aprobación antes de resumir; nunca eliminar automáticamente.'
        shutil.copy2(docs[chosen],dest/f'{stem}.docx');shutil.copy2(pdfs[chosen],dest/f'{stem}.pdf')
        render(dest/f'{stem}.pdf',dest/f'{stem}_paginas')
        save(dest/f'{stem}_validacion.json',report)
    return report

def preview(case):
    case=Path(case).resolve();cfg=load(case/'config.json');data=load(case/'cv_es.json');state=load(case/'estado.json')
    if state.get('contenido_aprobado')!=digest(case):raise ValueError('Aprobar contenido antes de mostrar la propuesta')
    name=DEFAULT_STYLE
    result=best(data,cfg,name,case/'propuestas'/name,'CV_ES',case)
    save(case/'propuestas'/'comparacion.json',{name:result})
    state['propuestas_hash']=digest(case);save(case/'estado.json',state)
    return {name:result}

def generate(case):
    case=Path(case).resolve();cfg=load(case/'config.json');state=load(case/'estado.json');current=digest(case)
    if state.get('contenido_aprobado')!=current or state.get('traduccion_aprobada')!=current:raise ValueError('Contenido y traducción deben revisarse después del último cambio')
    if state.get('estilo_aprobado')!=DEFAULT_STYLE or state.get('seleccion_hash')!=current:raise ValueError('Falta aprobar visualmente la plantilla seleccionada')
    es,en=load(case/'cv_es.json'),load(case/'cv_en.json')
    errors=bilingual(es,en)
    if errors:raise ValueError('\n'.join(errors))
    with tempfile.TemporaryDirectory(prefix='cv-final-') as scratch:
        out=Path(scratch)
        reports={lang:best(d,cfg,DEFAULT_STYLE,out,f'CV_{lang}',case) for lang,d in [('ES',es),('EN',en)]}
        save(out/'informe.json',{'estado':'PENDIENTE_REVISION_VISUAL','entrada_sha256':current,'idiomas':reports,
            'limites':['La IA en VS Code redacta, no está conectada desde Python.',
                       'DOCX puede cambiar al abrir en otro equipo o con otra fuente; validar allí.',
                       'Los avisos de confidencialidad no certifican que el contenido sea publicable.']})
        if not all(r['ok_tecnico'] for r in reports.values()):
            failed=case/'diagnostico'
            if failed.exists():shutil.rmtree(failed)
            shutil.copytree(out,failed)
            raise ValueError('Error de validación. Ver diagnostico/informe.json; no se han sustituido entregas previas.')
        target=case/'salida'
        if target.exists():
            archive=case/'historial';archive.mkdir(exist_ok=True)
            from datetime import datetime
            shutil.move(str(target),archive/datetime.now().strftime('%Y%m%d-%H%M%S-%f'))
        shutil.copytree(out,target)
        state.pop('revision_visual',None);state['ultima_generacion']=current;save(case/'estado.json',state)
    return reports
