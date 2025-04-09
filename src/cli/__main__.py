import argparse

from marktile.marktile import markdown_to_textile

from cli.__init__ import __project_name__, __project_description__, __project_version__

def main():

    # declara un HelpFormatter personalizado para reemplazar el texto 'usage:' por 'Uso:'
    class CustomHelpFormatter(argparse.HelpFormatter):
        def add_usage(self, usage, actions, groups, prefix='Uso: '):
            if usage is not argparse.SUPPRESS:
                args = usage, actions, groups, prefix
                self._add_item(self._format_usage, args)

    # define el parser
    parser = argparse.ArgumentParser(
        prog=__project_name__, 
        description=f"{__project_description__} (v{__project_version__})", 
        add_help=False, 
        epilog='Made with ❤️ by @fvarrui',
        formatter_class=CustomHelpFormatter
    )

    # define los comandos (mutuamente excluyentes)
    commands = parser.add_argument_group('Comandos')    
    commands = commands.add_mutually_exclusive_group(required=True)
    commands.add_argument('-h', '--help', action='store_true', help='Muestra esta ayuda y termina')
    commands.add_argument('-v', '--version', action='version', help='Mostrar versión', version=f'{__project_name__} v{__project_version__}')
    commands.add_argument('--file', metavar='FILE', help='Fichero en formato Markdown a convertir a Textile')

    # define las opciones
    options = parser.add_argument_group('Opciones')
    options.add_argument('--output', metavar='DIR', nargs='?', const='output', help='Directorio de destino para los ficheros convertidos')

    # parsea los argumentos
    args = parser.parse_args()

    # lógica según las opciones
    if args.help:
        parser.print_help()
        return

    if args.file:

        markdown_file = args.file
        markdown_to_textile(markdown_file, args.output)
        
if __name__ == "__main__":
    main()
