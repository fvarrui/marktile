# marktile

Conversor de Markdown a Textile en Python.

## ¿Qué hace?

Convierte un fichero en formato `.md` a `.textile`, remplazando los bloques [PlantUML](https://plantuml.com/) y [Mermaid](https://mermaid.js.org/) por imágenes.

## ¿Cómo se usa?

```bash
$ marktile --file fichero.md --output destino
```

> ℹ️ Si no se especifica el directorio de destino, la salida se genera en el directorio actual.

Para obtener ayuda sobre cómo usar el comando, se puede utilizar la opción `--help`:

```bash
$ marktile --help

Uso: marktile (-h | -v | --file FILE) [--output [DIR]]

Markdown to Textile converter (v0.1.2)

Comandos:
  -h, --help      Muestra esta ayuda y termina
  -v, --version   Mostrar versión
  --file FILE     Fichero en formato Markdown a convertir a Textile

Opciones:
  --output [DIR]  Directorio de destino para los ficheros convertidos
```

### Ejemplo de uso

Partiendo del documento [`test.md`](tests/test.md) en formato Markdown, que contiene tablas, listas y diagramas en formato `Mermaid` y `PlantUML`, ejecutamos `marktile` dándole como entrada el fichero `test.md` (`--file`) e indicándole que la salida la genere en el directorio `.` (`--output`) en este caso, mostrando la siguiente salida:

```bash
$ marktile --file test.md --output .
Convirtiendo fichero Markdown a Textile...
Fichero de entrada           : test.md
Directorio de salida         : .
Imagenes generadas para bloques: ['.\\test_1.png', '.\\test_2.png']
Fichero Textile generado     : .\test.textile
```

Esto generará el fichero [`test.textile`](/tests/test.textile) y una imagen `test_*.png` por cada diagrama, en el directorio indicado (en este caso, el directorio actual `--output .`). Las imágenes generadas serían las siguientes:

- [`test_1.png`](tests/test_1.png) para el diagrama `mermaid`
- [`test_2.png`](tests/test_2.png) para el diagrama `plantuml`

