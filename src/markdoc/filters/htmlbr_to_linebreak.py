import panflute as pf

def action(elem, doc):
    if isinstance(elem, pf.RawInline) and elem.format == 'html':
        if elem.text.strip().lower() in ('<br>', '<br/>', '<br />'):
            return pf.RawInline('<text:line-break/>', format='opendocument')

def main(doc=None):
    return pf.run_filter(action, doc=doc)

if __name__ == "__main__":
    main()
