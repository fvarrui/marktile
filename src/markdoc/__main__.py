import os
import sys
from markdoc.markdoc import md_to_odt

def main():
    if len(sys.argv) < 3:
        print("Uso: markdoc <input_file> <output_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    print(f"Archivo MD de entrada: {input_file}")
    md_to_odt(input_file, output_file)
    os.startfile(output_file)
    print(f"Archivo ODT generado: {output_file}")

if __name__ == "__main__":
    main()