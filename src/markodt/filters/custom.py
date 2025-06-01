import panflute as pf

def action(elem, doc):
    if isinstance(elem, pf.Table):
        elem.attributes['custom-style'] = 'Estilo de tabla predeterminado'

def main(doc=None):
    return pf.run_filter(action, doc=doc)

if __name__ == '__main__':
    main()
