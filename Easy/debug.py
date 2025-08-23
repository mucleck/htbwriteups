import re
import sys
import os

def convertir_markdown_a_estandar(ruta_md):
    if not os.path.exists(ruta_md):
        print(f"❌ Archivo no encontrado: {ruta_md}")
        return

    with open(ruta_md, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Buscar todas las imágenes tipo Obsidian: ![[ruta/imagen.png]]
    patron = r'!\[\[(.*?)\]\]'
    coincidencias = re.findall(patron, contenido)

    if not coincidencias:
        print("ℹ️ No se encontraron imágenes en formato Obsidian.")
        return

    for path in coincidencias:
        nombre = os.path.splitext(os.path.basename(path))[0]  # sin extensión
        markdown_estandar = f'![{nombre}]({path})'
        contenido = contenido.replace(f'![[{path}]]', markdown_estandar)

    with open(ruta_md, 'w', encoding='utf-8') as f:
        f.write(contenido)

    print(f"✅ Conversión completada para: {ruta_md}")

# Uso desde terminal
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python convertir_a_markdown_estandar.py archivo.md")
    else:
        convertir_markdown_a_estandar(sys.argv[1])
