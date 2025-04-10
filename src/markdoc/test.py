import os
import pypandoc

def odt_2_md():
    # Ruta al archivo .odt
    input_file = "C:\\Users\\fvarrui\\Desktop\\XXXX-XXXX_AFS_Análisis_funcional_del_sistema.odt"
    # Convertir a Markdown
    markdown = pypandoc.convert_file(input_file, to='gfm', encoding='utf-8')
    # Guardar el resultado en un archivo .md
    with open("XXXX-XXXX_AFS_Análisis_funcional_del_sistema.md", "w", encoding="utf-8") as f:
        f.write(markdown)
    print("Conversión completada.")


def md_to_odt():
   
    # Ruta al archivo .md
    input_file = "XXXX-XXXX_AFS_Análisis_funcional_del_sistema.md"
    # Convertir a ODT
    output_file = "XXXX-XXXX_AFS_Análisis_funcional_del_sistema.odt"
    pypandoc.convert_file(
        input_file, 
        to='odt', 
        outputfile=output_file, 
        extra_args=[            
            '--reference-doc=template.odt',
            '--toc',
            '--toc-depth=3',
            '--standalone',
            '--lua-filter=filters/pagebreak.lua',
            '--lua-filter=filters/diagram.lua',
            '--metadata=image-width:100%',            
        ]
    )
    print("Conversión completada.")

md_to_odt()
os.startfile("XXXX-XXXX_AFS_Análisis_funcional_del_sistema.odt")