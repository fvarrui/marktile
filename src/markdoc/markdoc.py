import os
import pypandoc

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PYTHON_FILTERS = [
    "add_pagebreak_before_h1.py",
    "htmlbr_to_linebreak.py",
    "custom.py",
];
LUA_FILTERS = [
    "diagram.lua",
];
ODT_TEMPLATE = "templates/template.odt"
CONTENT_TEMPLATE = "templates/default.opendocument.xml"

def md_to_odt(input_file, output_file):
    template_path =  os.path.join(BASE_DIR, ODT_TEMPLATE)
    content_xml_path = os.path.join(BASE_DIR, CONTENT_TEMPLATE)
    extra_args = [
        "--quiet",
        "--standalone",
        f"--reference-doc={template_path}",     # plantilla de referencia para coger estilos, encabezado y pie de página
        f"--template={content_xml_path}",       # plantilla de contenido
        "--toc",
    ]
    # Añadir filtros de Python
    for filter_name in PYTHON_FILTERS:
        filter_path = os.path.join(BASE_DIR, "filters", filter_name)
        extra_args.append(f"--filter={filter_path}")
    # Añadir filtros de Lua
    for filter_name in LUA_FILTERS:
        filter_path = os.path.join(BASE_DIR, "filters", filter_name)
        extra_args.append(f"--lua-filter={filter_path}")
    pypandoc.convert_file(
        format="gfm",  # formato de entrada, puede ser "markdown", "gfm" (GitHub Flavored Markdown), etc.
        to="odt",  # formato de salida
        source_file=input_file,
        outputfile=output_file,
        extra_args=extra_args,
    )
