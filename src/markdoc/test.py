import os
import pypandoc
import json

def odt_to_markdown():
    # Ruta al archivo .odt
    input_file = "XXXX-XXXX_AFS_Análisis_funcional_del_sistema.odt"
    # Convertir a Markdown
    markdown = pypandoc.convert_file(input_file, to="gfm", encoding="utf-8")
    # Guardar el resultado en un archivo .md
    with open("XXXX-XXXX_AFS_Análisis_funcional_del_sistema.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    print("Conversión completada.")

def md_to_odt():

    # Ruta al archivo .md
    input_file = "ejemplo.md"
    # Convertir a ODT
    output_file = "ejemplo.odt"
    pypandoc.convert_file(
        to="odt",
        source_file=input_file,
        outputfile=output_file,
        extra_args=[
            "--quiet",
            "--standalone",
            "--template=templates/template.opendocument.xml", # plantilla para el contenido del documento
            "--reference-doc=templates/template.odt", # plantilla de referencia para coger estilos, encabezado y pie de página
            "--toc",
            "--metadata=title:",
            "--metadata=subtitle:",
            "--metadata=author:",
            "--metadata=date:",
            "--metadata=sample:Hola qué tal",
            #'--lua-filter=filters/diagram.lua',
            #'--filter=filters/pagebreak.py',
            #'--filter=filters/diagram.py',
            #'--lua-filter=filters/pagebreak.lua',
            #'--lua-filter=filters/revisions.lua',
            #"--filter=filters/mi_filtro.py",
        ],
    )
    print("Conversión completada.")


md_to_odt()
os.startfile("ejemplo.odt")

