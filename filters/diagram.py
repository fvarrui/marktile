# Conversión del filtro diagram.lua a Python usando Panflute
# Requiere: panflute, plantuml/dot/mmdc/pdflatex/asy/inkscape instalados según el motor usado

import os
import hashlib
import panflute as pf
import tempfile
import subprocess

# MIME y extensiones
mimetypes = {
    'svg': 'image/svg+xml',
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'pdf': 'application/pdf'
}
extensions = {v: k for k, v in mimetypes.items()}

# Utilidades
def sha1(data):
    return hashlib.sha1(data if isinstance(data, bytes) else data.encode()).hexdigest()

def write_file(path, content, mode='wb'):
    with open(path, mode) as f:
        f.write(content if isinstance(content, bytes) else content.encode())

# Motores
def compile_plantuml(code, mime='image/svg+xml'):
    fmt = extensions.get(mime, 'svg')
    result = subprocess.run(['plantuml', f'-t{fmt}', '-pipe'], input=code.encode(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode())
    return result.stdout, mime

# Motores disponibles
engines = {
    'plantuml': compile_plantuml,
}

# Extracción de atributos
def parse_attrs(cb):
    attribs = {**cb.attributes}
    fig_attr = {'id': cb.identifier}
    image_attr = {}
    caption = None
    alt = []

    if 'caption' in attribs:
        caption = pf.convert_text(attribs['caption'], input_format='markdown').blocks
        alt = pf.stringify(caption)
    if 'alt' in attribs:
        alt = attribs['alt']

    return fig_attr, image_attr, caption, alt

# Conversión de bloque
def convert_codeblock(elem, doc):
    if not isinstance(elem, pf.CodeBlock):
        return
    if not elem.classes:
        return
    engine_name = elem.classes[0]
    if engine_name not in engines:
        return

    fig_attr, image_attr, caption, alt = parse_attrs(elem)

    mime = 'image/png'  # Formato predeterminado
    try:
        imgdata, actual_mime = engines[engine_name](elem.text, mime)
    except Exception as e:
        pf.debug(f"Error al procesar '{engine_name}': {e}")
        return

    # Guardar la imagen en un archivo temporal
    hashname = sha1(imgdata)
    ext = extensions[actual_mime]
    tmpdir = tempfile.gettempdir()
    fname = os.path.join(tmpdir, f'{hashname}.{ext}')
    write_file(fname, imgdata)

    # Crear el elemento de imagen
    img = pf.Image(pf.stringify(alt), fname, title="", attributes=image_attr)

    # Convertir la lista de bloques de caption a un único bloque de texto
    if caption:
        caption_text = pf.stringify(caption)  # Convierte los bloques en texto plano
        return pf.Figure(pf.Plain(img), pf.Plain(pf.Str(caption_text)), attributes=fig_attr)

    return pf.Plain(img)

# Filtro principal
def main(doc=None):
    return pf.run_filter(convert_codeblock, doc=doc)

if __name__ == "__main__":
    main()