from panflute import *

def prepare(doc):
    pass  # No se necesita preparación para este filtro

def action(elem, doc):
    if isinstance(elem, Table):
        # Añadir estilo de tabla
        elem.attributes['custom-style'] = 'Estilo de tabla predeterminado'

        # Procesar celdas del encabezado
        table_head = elem.head
        if table_head:
            for row in table_head.rows:
                for cell in row.cells:
                    new_blocks = []
                    for block in cell.content:
                        if isinstance(block, Para):
                            new_block = Para(*block.content, attributes={"custom-style": "Encabezado"})
                            new_blocks.append(new_block)
                        else:
                            new_blocks.append(block)
                    cell.content = new_blocks

    return elem

def finalize(doc):
    pass  # No limpieza final necesaria

def main():
    run_filter(action, prepare=prepare, finalize=finalize)

if __name__ == "__main__":
    main()
