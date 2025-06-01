#!/usr/bin/env python

import sys
import panflute as pf

def action(elem, doc):
    # Verificar si el elemento es un párrafo que contiene [[REVISIONS]]
    if isinstance(elem, pf.Para):
        #print(f"Párrafo: {elem}", file=sys.stderr)
        # Buscar [[REVISIONS]] dentro del contenido del párrafo
        if any(isinstance(inline, pf.Str) and inline.text == "\\revisions" for inline in elem.content):
            # Reemplazar el párrafo completo con un nuevo contenido
            return pf.Para(
                pf.Str("Revisión 1: Creación del documento"),
                pf.LineBreak(),
                pf.Str("Revisión 2: Modificación del documento")
            )

def main(doc=None):
    print("Ejecutando el filtro de revisiones...", file=sys.stderr)
    return pf.run_filter(action, doc=doc)

if __name__ == "__main__":
    main()
