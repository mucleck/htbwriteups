import os
import re
import sys

def actualizar_imagenes(ruta_md):
    if not os.path.exists(ruta_md):
        print(f"❌ Archivo no encontrado: {ruta_md}")
        return

    nombre_base = os.path.splitext(os.path.basename(ruta_md))[0]
    directorio_md = os.path.dirname(os.path.abspath(ruta_md))
    ruta_img = os.path.abspath(os.path.join(directorio_md, '../img'))

    if not os.path.exists(ruta_img):
        print(f"❌ Carpeta de imágenes no encontrada: {ruta_img}")
        return

    with open(ruta_md, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Nuevo patrón que detecta: ![[Pasted image 20250822204719.png]]
    patron = r'!\[\[(Pasted image \d{10,16}\.png)\]\]'
    coincidencias = re.findall(patron, contenido)

    if not coincidencias:
        print("ℹ️ No se encontraron imágenes con ese patrón.")
        return

    imagenes_renombradas = {}
    for i, original in enumerate(coincidencias, start=1):
        nuevo_nombre = f'{nombre_base}_{i}.png'

        ruta_origen = os.path.join(ruta_img, original)
        ruta_destino = os.path.join(ruta_img, nuevo_nombre)

        if os.path.exists(ruta_origen):
            os.rename(ruta_origen, ruta_destino)
            print(f"✅ Renombrado: {original} → {nuevo_nombre}")
        else:
            print(f"⚠️ Imagen no encontrada en ../img/: {original}")

        imagenes_renombradas[original] = nuevo_nombre

    # Reemplazar en el contenido del .md
    for original, nuevo in imagenes_renombradas.items():
        viejo = f'![[{original}]]'
        nuevo_md = f'![[../img/{nuevo}]]'
        contenido = contenido.replace(viejo, nuevo_md)

    # Guardar el archivo actualizado
    with open(ruta_md, 'w', encoding='utf-8') as f:
        f.write(contenido)

    print(f"\n✅ Archivo Markdown actualizado: {ruta_md}")

# Ejecutar desde terminal
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python actualizar_md.py archivo.md")
    else:
        actualizar_imagenes(sys.argv[1])

