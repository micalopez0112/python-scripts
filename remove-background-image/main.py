#pip install rembg onnxruntime

from rembg import remove

def remove_background(input_path, output_path):
    with open(input_path, 'rb') as i:
        input_data = i.read()
        output_data = remove(input_data)

    with open(output_path, 'wb') as o:
        o.write(output_data)

    print(f"Foto salvada en: {output_path}")

remove_background("foto.jpg", "foto_sin_fondo.png")
