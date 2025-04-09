import base64
import io, requests
from PIL import Image as im
import matplotlib.pyplot as plt

MERMAID_URL = "https://mermaid.ink/img"

def mermaid_to_image(code: str, output_file: str):
    graphbytes = code.encode("utf8")
    base64_bytes = base64.urlsafe_b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    
    # Descargar la imagen desde Mermaid
    img = im.open(io.BytesIO(requests.get(f"{MERMAID_URL}/{base64_string}").content))
    
    # Recortar la imagen para eliminar los bordes sobrantes
    img = img.crop(img.getbbox())  # Recorta según el contenido no vacío
    
    # Guardar la imagen recortada
    img.save(output_file, dpi=(300, 300))
