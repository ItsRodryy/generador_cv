"""Local CLI; AI interview is performed in VS Code by Codex/Claude after user answers."""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from .modelo import ROOT,load,save,initial_config,digest,check,bilingual
from .importar import extract
from .componer import style,DEFAULT_STYLE
from .pipeline import preview,generate,STYLES,best
from .exportar import office
from .seguridad import warnings as confidentiality_warnings

EDITABLE={'header_bg','header_radius','header_pad','name','role','contact','photo_pt','wave_color','wave_amplitude',
          'wave_thickness','icon_color','icon_pt','icons','divider_color','separator','body','title','section',
          'block_gap','section_gap','leading','margin','repeat_name','footer','compactness'}

def main(argv=None):
    parser=argparse.ArgumentParser(description='Generador CV: Minimalista Onda ES/EN · Codex / Claude Code')
    sub=parser.add_subparsers(dest='cmd',required=True)
    p=sub.add_parser('nuevo',help='Crear caso privado');p.add_argument('caso',type=Path)
    p=sub.add_parser('importar',help='Preservar original y extraer PDF/DOCX');p.add_argument('archivo',type=Path);p.add_argument('--caso',required=True,type=Path)
    sub.add_parser('doctor',help='Revisar dependencias')
    p=sub.add_parser('plantilla',help='Mostrar plantilla con caso ficticio sin datos privados');p.add_argument('--salida',type=Path,required=True)
    for command in ('estado','preguntas','aprobar','propuestas','elegir','generar','cerrar','configurar','visual','confidencialidad'):
        p=sub.add_parser(command);p.add_argument('--caso',required=True,type=Path)
        if command=='aprobar':p.add_argument('parte',choices=('contenido','traduccion'))
        if command=='elegir':p.add_argument('estilo',choices=STYLES)
        if command=='configurar':
            p.add_argument('campo',help='paginas, fuente, foto, foto_confirmada o visual.<campo>');p.add_argument('valor')
        if command=='cerrar':
            p.add_argument('--revisor',required=True);p.add_argument('--confirmo-inspeccion-visual',action='store_true')
    args=parser.parse_args(argv)
    try:
        if args.cmd=='doctor':
            print('Python:',sys.version.split()[0]);print('Conversor:',office());print('Estilos:',', '.join(STYLES));return 0
        if args.cmd=='plantilla':
            demo=ROOT/'ejemplos'/'caso_ficticio';dest=args.salida.resolve();dest.mkdir(parents=True,exist_ok=True)
            cfg=load(demo/'config.json');cfg['estilo']=DEFAULT_STYLE;cfg['fuente']='Lato'
            result=best(load(demo/'cv_es.json'),cfg,DEFAULT_STYLE,dest,'CV_DEMO',demo)
            print(json.dumps({'ok':result['ok_tecnico'],'errores':result['errores'],'vista_previa':str(dest)},ensure_ascii=False,indent=2))
            return 0 if result['ok_tecnico'] else 2
        case=args.caso.resolve()
        if args.cmd=='nuevo':
            if case.exists():raise ValueError('La carpeta ya existe, no se sobrescribe')
            case.mkdir(parents=True)
            save(case/'config.json',initial_config());save(case/'estado.json',{'fase':'importar','decisiones':[],'pendientes':[]})
            (case/'PREGUNTAS_Y_DECISIONES.md').write_text('# Decisiones del caso\n\nAnotar preguntas, respuestas y aprobaciones.\n',encoding='utf-8')
            print('Caso creado. Importa cualquier CV PDF/DOCX o trabaja desde cero.');return 0
        if not (case/'config.json').is_file():raise ValueError('Caso no inicializado: usa nuevo')
        if args.cmd=='importar':print(extract(args.archivo,case))
        elif args.cmd=='estado':print((case/'estado.json').read_text(encoding='utf-8'));print('SHA256:',digest(case))
        elif args.cmd=='preguntas':
            cfg=load(case/'config.json')
            print('Entrevista adaptable. El asistente lee extracción, estado y PREGUNTAS_Y_DECISIONES.md y no repite respuestas:')
            for q in ('¿Qué puesto/sector y perfil general quieres destacar?', '¿Qué datos de tu CV importado debemos confirmar?',
                      '¿Qué experiencia, proyectos o competencias modificar?', '¿Quieres español, inglés o ambos (salida admite ambos)?',
                      f'¿Cuántas páginas A4 deseas? (actual: {cfg["paginas"]}; entre 1 y 4)',
                      '¿Usamos la fotografía encontrada? ¿Autoriza su inclusión?',
                      'Aquí tienes la plantilla Minimalista Onda: ¿qué modificarías en foto, borde, cabecera, colores o tipografía?',
                      '¿Quieres cambiar el orden, iconos, separadores y tamaño de cada sección?',
                      '¿Existen nombres de clientes, código interno, IPs, métricas o material confidencial que debamos eliminar?',
                      '¿Has revisado la traducción, los enlaces y todas las páginas de la previsualización?'):
                print('•',q)
            print('Usa `python -m generador_cv plantilla --salida vistas_demo` para enseñar la plantilla sin datos personales.')
        elif args.cmd=='visual':print(json.dumps(style(DEFAULT_STYLE,load(case/'config.json').get('visual')),ensure_ascii=False,indent=2))
        elif args.cmd=='configurar':
            cfg=load(case/'config.json');key=args.campo;raw=args.valor
            if key=='paginas':
                if not raw.isdigit() or not 1<=int(raw)<=4:raise ValueError('paginas: entero de 1 a 4')
                cfg['paginas']=int(raw)
            elif key=='fuente':cfg['fuente']=raw
            elif key=='foto':cfg['foto']=None if raw.lower() in ('none','null','sin') else raw
            elif key=='foto_confirmada':cfg['foto_confirmada']=raw.lower() in ('true','1','si','sí')
            elif key.startswith('visual.') and key[7:] in EDITABLE:
                attr=key[7:]
                if raw.lower() in ('true','false'):val=raw.lower()=='true'
                elif attr not in ('header_bg','wave_color','icon_color','divider_color','separator','footer'):
                    try:val=float(raw)
                    except ValueError:raise ValueError('Esperado valor numérico o booleano')
                else:val=raw
                cfg.setdefault('visual',{})[attr]=val
                style(DEFAULT_STYLE,cfg.get('visual'))
            else:raise ValueError('Campo no configurable; consulta visual y docs/ESTILO.md')
            save(case/'config.json',cfg)
            # State approvals are content-dependent and invalidated through the digest.
            print('Configuración guardada; debes regenerar vistas y volver a aprobar cualquier cambio.')
        elif args.cmd=='confidencialidad':
            for lang in ('es','en'):
                p=case/f'cv_{lang}.json'
                if p.exists():
                    for w in confidentiality_warnings(load(p)):print(lang,w)
            print('Advertencias orientativas: el usuario debe revisar permisos y políticas antes de publicar.')
        elif args.cmd=='aprobar':
            es=load(case/'cv_es.json');check(es)
            if args.parte=='traduccion':
                errors=bilingual(es,load(case/'cv_en.json'))
                if errors:raise ValueError('\n'.join(errors))
            state=load(case/'estado.json');state['contenido_aprobado' if args.parte=='contenido' else 'traduccion_aprobada']=digest(case)
            save(case/'estado.json',state);print('Revisión DECLARADA. Debe haberse efectuado antes de ejecutar aprobar.')
        elif args.cmd=='propuestas':
            result=preview(case)
            for name,report in result.items():print(name,report['estado'],'; '.join(report['errores']))
            return 0 if all(r['ok_tecnico'] for r in result.values()) else 2
        elif args.cmd=='elegir':
            state=load(case/'estado.json');old=digest(case)
            if state.get('propuestas_hash')!=old:raise ValueError('Primero previsualiza el contenido actual')
            report=load(case/'propuestas'/args.estilo/'CV_ES_validacion.json')
            if not report['ok_tecnico']:raise ValueError('La propuesta tiene errores; revisa antes')
            cfg=load(case/'config.json');cfg['estilo']=args.estilo;save(case/'config.json',cfg)
            new=digest(case)
            for key in ('contenido_aprobado','traduccion_aprobada','propuestas_hash'):
                if state.get(key)==old:state[key]=new
            state['estilo_aprobado']=args.estilo;state['seleccion_hash']=new;save(case/'estado.json',state)
            print('Plantilla seleccionada. Confirma su apariencia en las páginas renderizadas antes de generar finales.')
        elif args.cmd=='generar':
            generate(case);print('CV_ES / CV_EN (PDF + DOCX) generados; inspección visual aún obligatoria.')
        elif args.cmd=='cerrar':
            if not args.confirmo_inspeccion_visual:raise ValueError('Falta --confirmo-inspeccion-visual; no declarar revisión no realizada')
            st=load(case/'estado.json')
            if st.get('ultima_generacion')!=digest(case):raise ValueError('Cambió la entrada; regenerar')
            rep=load(case/'salida'/'informe.json')
            if not all(r['ok_tecnico'] for r in rep['idiomas'].values()):raise ValueError('Errores técnicos')
            hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (case/'salida').glob('CV_*.*')}
            st['revision_visual']={'revisor':args.revisor,'archivos_sha256':hashes};save(case/'estado.json',st)
            rep['estado']='REVISADO_VISUALMENTE';rep['revision_visual_declarada']=st['revision_visual'];save(case/'salida'/'informe.json',rep)
            print('Revisión declarada por el usuario; no constituye certificación automática.')
        return 0
    except (ValueError,RuntimeError,OSError,KeyError) as ex:
        print('ERROR:',ex,file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
