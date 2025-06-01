import os
import sys
import glob
from markodt.markodt import md_to_odt

def main():
    if len(sys.argv) < 3:
        print("Uso: markodt <input_file...> <output_file>")
        sys.exit(1)
    input_pattern = sys.argv[1]
    output_file = sys.argv[2]
    input_files = glob.glob(input_pattern)
    print(f"Archivos MD de entrada: {input_files}")
    md_to_odt(input_files, output_file)
    os.startfile(output_file)
    print(f"Archivo ODT generado: {output_file}")

if __name__ == "__main__":
    main()