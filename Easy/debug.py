import re
import sys

def encontrar_imagenes(ruta_md):
    with open(ruta_md, 'r', encoding='utf-8') as f:
        contenido = f.read()

    patron = r'!\[\[(Pasted image \d{12}\.png)\]\]'
    coincidencias = re.findall(patron, contenido)

    if not coincidencias:
        print("❌ No se encontraron coincidencias.")
    else:
        print("✅ Coincidencias encontradas:")
        for c in coincidencias:
            print(f" - {c}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python debug_md.py archivo.md")
    else:
        encontrar_imagenes(sys.argv[1])
