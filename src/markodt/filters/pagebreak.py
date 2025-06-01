import os
import panflute as pf

# Configuraciones de salto de página por formato
DEFAULT_PAGEBREAKS = {
    'asciidoc': '<<<\n\n',
    'context': '\\page',
    'epub': '<p style="page-break-after: always;"> </p>',
    'html': '<div style="page-break-after: always;"></div>',
    'latex': '\\newpage{}',
    'ms': '.bp',
    'ooxml': '<w:p><w:r><w:br w:type="page"/></w:r></w:p>',
    'odt': '<text:p text:style-name="Pagebreak"/>',
    'typst': '#pagebreak()\n\n'
}

# Global
raw_pagebreak = None
paragraph_checks = []

def pagebreak_from_config(meta):
    pagebreak = DEFAULT_PAGEBREAKS.copy()

    html_class = meta.get('html-class', None)
    if html_class:
        html_class = pf.stringify(html_class)
    else:
        html_class = os.getenv('PANDOC_PAGEBREAK_HTML_CLASS')

    if html_class:
        pagebreak['html'] = f'<div class="{html_class}"></div>'

    odt_style = meta.get('odt-style', None)
    if odt_style:
        odt_style = pf.stringify(odt_style)
    else:
        odt_style = os.getenv('PANDOC_PAGEBREAK_ODT_STYLE')

    if odt_style:
        pagebreak['odt'] = f'<text:p text:style-name="{odt_style}"/>'

    return pagebreak

def newpage(format, pagebreaks):
    format = format.lower()
    if 'asciidoc' in format:
        return pf.RawBlock(pagebreaks['asciidoc'], format='asciidoc')
    elif format == 'context':
        return pf.RawBlock(pagebreaks['context'], format='context')
    elif format == 'docx':
        return pf.RawBlock(pagebreaks['ooxml'], format='openxml')
    elif 'epub' in format:
        return pf.RawBlock(pagebreaks['epub'], format='html')
    elif 'html' in format:
        return pf.RawBlock(pagebreaks['html'], format='html')
    elif 'latex' in format:
        return pf.RawBlock(pagebreaks['latex'], format='tex')
    elif 'ms' in format:
        return pf.RawBlock(pagebreaks['ms'], format='ms')
    elif 'odt' in format:
        return pf.RawBlock(pagebreaks['odt'], format='opendocument')
    elif 'typst' in format:
        return pf.RawBlock(pagebreaks['typst'], format='typst')
    else:
        return pf.Para(pf.Str('\f'))

def is_newpage_command(text):
    return text in ['\\newpage', '\\newpage{}', '\\pagebreak', '\\pagebreak{}']

def latex_pagebreak(elem, doc):
    if isinstance(elem, pf.RawBlock) and elem.format in ('tex', 'latex'):
        if is_newpage_command(elem.text):
            return raw_pagebreak

def formfeed_check(para):
    return (len(para.content) == 1 and isinstance(para.content[0], pf.Str)
            and para.content[0].text == '\f')

def plaintext_check(para):
    return (len(para.content) == 1 and isinstance(para.content[0], pf.Str)
            and is_newpage_command(para.content[0].text))

def para_pagebreak(elem, doc):
    if isinstance(elem, pf.Para):
        for check in paragraph_checks:
            if check(elem):
                return raw_pagebreak

def prepare(doc):
    global raw_pagebreak, paragraph_checks

    config = doc.get_metadata('pagebreak', {})
    break_on = config.get('break-on', {})

    pagebreaks = pagebreak_from_config(doc.metadata)
    raw_pagebreak = newpage(doc.format, pagebreaks)

    paragraph_checks = []
    if break_on.get('form-feed'):
        paragraph_checks.append(formfeed_check)
    if break_on.get('plaintext-command'):
        paragraph_checks.append(plaintext_check)

    if 'pagebreak' in doc.metadata:
        del doc.metadata['pagebreak']

def main(doc=None):
    return pf.run_filters(
        [latex_pagebreak, para_pagebreak],
        prepare=prepare,
        doc=doc
    )

if __name__ == "__main__":
    main()