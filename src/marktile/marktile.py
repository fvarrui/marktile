import os
import pypandoc

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdformat.renderer import MDRenderer
import mdformat_tables

from .plantuml import plantuml_to_image
from .mermaid import mermaid_to_image

def markdown_to_textile(markdown_file: str, output_dir: str = 'output') -> None:
    """
    Convierte un texto en formato Markdown a formato Textile.
    - Parámetros:
        - markdown_text: Texto en formato Markdown.
    - Retorno:
        - Texto en formato Textile.
    """

    print("Convirtiendo fichero Markdown a Textile...")
    print("Fichero de entrada           :", markdown_file)
    print("Directorio de salida         :", output_dir)

    # Crea el directorio de destino si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Lee el fichero Markdown
    with open(markdown_file, 'r', encoding='utf-8') as file:
        markdown_text = file.read()

    # Obtiene el directorio de destino
    textile_file = os.path.basename(markdown_file).replace('.md', '.textile')
    textile_file = os.path.join(output_dir, textile_file)

    # Obtiene el prefijo para las imágenes
    img_prefix = os.path.basename(textile_file).replace('.textile', '')

    # Extrae los bloques de PlantUML
    markdown_text = replace_fences_with_images(markdown_text, output_dir, img_prefix)

    # Guardar el nuevo markdown
    #new_markdown_file = os.path.join(output_dir, os.path.basename(markdown_file))    
    #with open(new_markdown_file, 'w', encoding='utf-8', newline='\n') as file:
    #    file.write(markdown_text)
    #print("Fichero Markdown generado    :", new_markdown_file)

    # Convierte el texto de Markdown a Textile
    textile_text = pypandoc.convert_text(markdown_text, 'textile', format='md')

    # Escribe el fichero Textile
    with open(textile_file, 'w', encoding='utf-8', newline='\n') as file:
        file.write(textile_text)
    print("Fichero Textile generado     :", textile_file)


def replace_fences_with_images(markdown_text: str, output_dir: str, img_prefix: str = '') -> str:
    """
    Extrae los bloques de PlantUML de un texto en formato Markdown.
    - Parámetros:
        - markdown_text: Texto en formato Markdown.
    - Retorno:
        - Texto en formato Markdown sin los bloques de PlantUML.
    """

    # Parsea el texto en formato Markdown
    md = MarkdownIt(config='gfm-like').enable('table')
    tokens = md.parse(markdown_text)

    # Remplaza los bloques de PlantUML por imágenes
    new_tokens = []
    images = []
    images_count = 0
    for token in tokens:
        if token.type == 'fence' and token.info in FENCES_TO_IMAGES:
            
            images_count += 1

            image_file = os.path.join(output_dir, f'{img_prefix}_{images_count}.png')
            FENCES_TO_IMAGES[token.info](token.content, image_file)
            images.append(image_file)

            # Crear un token para la imagen
            img_token = Token("image", "", 0) 
            img_token.attrs = {"src": os.path.basename(image_file), "alt": "Diagrama generado"}
            new_tokens.append(img_token)
        else:
            new_tokens.append(token)

    print("Imagenes generadas para bloques:", images)

    # Renderiza el texto en formato Markdown
    renderer = MDRenderer()
    markdown_text = renderer.render(new_tokens, options = {
        "parser_extension": [mdformat_tables]
    }, env = {})

    return markdown_text

FENCES_TO_IMAGES = {
    'plantuml': plantuml_to_image,
    'mermaid': mermaid_to_image,
}