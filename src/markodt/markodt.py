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

def remove_frontmatter(markdown: str) -> str:
    """
    Elimina el frontmatter de un string Markdown.
    El frontmatter se define como el bloque entre dos líneas con "---".
    """
    if markdown.startswith("---"):
        end_index = markdown.find("---", 3)
        if end_index != -1:
            return markdown[end_index + 3:].strip()
    return markdown.strip()

def md_to_odt(input_files : list[str], output_file: str):
    """
    Convierte archivos Markdown a ODT utilizando Pandoc.
    :param input_files: Lista de archivos Markdown de entrada.
    :param output_file: Archivo ODT de salida.
    """

    template_path =  os.path.join(BASE_DIR, ODT_TEMPLATE)
    content_xml_path = os.path.join(BASE_DIR, CONTENT_TEMPLATE)

    # Parámetros adicionales para la conversión
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

    # Combinar el contenido de los archivos de entrada
    content = ""
    for idx, input_file in enumerate(input_files):
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"El archivo de entrada {input_file} no existe.")
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown = f.read()
            if idx > 0:
                markdown = remove_frontmatter(markdown)
            content += markdown + "\n\n"

    # Guardar el contenido combinado en un archivo temporal
    input_file = os.path.join(BASE_DIR, "temp.md")
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(content)

    # Convertir el archivo Markdown a ODT        
    pypandoc.convert_file(
        format="gfm",  # formato de entrada, puede ser "markdown", "gfm" (GitHub Flavored Markdown), etc.
        to="odt",  # formato de salida
        source_file=input_file,
        outputfile=output_file,
        extra_args=extra_args,
    )
