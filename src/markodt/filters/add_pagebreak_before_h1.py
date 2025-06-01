import panflute as pf

def action(elem, doc):
    if isinstance(elem, pf.Header) and elem.level == 1:
        pagebreak = pf.RawBlock('<text:p text:style-name="Pagebreak"/>', format='opendocument')
        return [pagebreak, elem]

def main(doc=None):
    return pf.run_filter(action, doc=doc)

if __name__ == '__main__':
    main()
