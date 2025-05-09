import sys
from panflute import *

sys.stderr = open("debug.log", "w", encoding="utf-8")

def prepare(doc: Doc) -> Doc:
    doc.revisions = doc.get_metadata("revisions", [])
    debug(f"Documento preparado {doc}", doc.revisions)    

def action(elem, doc):
    debug(f"Ejecutando... {elem}")
    if isinstance(elem, RawBlock) and elem.text == "\\revisions":
        # Reemplazar el bloque RawBlock con un nuevo contenido
        revisions = doc.revisions
        table_header = """
| **Fecha**      | **Descripción del cambio**     | **Autor**            |
| ---------- | -------------------------- | ---------------- |
"""
        table_body = ""
        for revision in revisions:
            table_body += f"| {revision['date']} | {revision['description']} | {revision['author']} |\n"
        return convert_text(table_header + table_body)
    return elem

def main(doc=None):
    debug(f"Ejecutando filtro")
    return run_filter(action, prepare=prepare)

if __name__ == "__main__":
    main()
