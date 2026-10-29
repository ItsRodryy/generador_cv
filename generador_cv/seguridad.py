"""Conservative, non-blocking publication warnings. NOT a confidentiality certification."""
import re
from .modelo import block_text

def warnings(data):
    issues=[]
    for b in data.get('blocks',[]):
        text=' '.join(block_text(b))
        if re.search(r'\b(?:10|172|192)\.(?:\d{1,3}\.){2}\d{1,3}\b',text):issues.append((b['id'],'Posible IP privada'))
        if re.search(r'https?://(?:localhost|[^ ]+\.(?:local|internal|lan))\b',text,re.I):issues.append((b['id'],'Posible URL interna'))
        if re.search(r'\b(?:contraseña|password|token|api[_ -]?key|secreto)\s*[:=]',text,re.I):issues.append((b['id'],'Posible credencial o información sensible'))
        if re.search(r'\b(?:cliente|customer)\s*[:=]',text,re.I):issues.append((b['id'],'Verificar permiso para mencionar cliente'))
    return [{'bloque':bid,'advertencia':message} for bid,message in issues]
