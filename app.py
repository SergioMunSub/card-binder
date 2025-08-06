from flask import Flask, render_template
import os
import json
import re

app = Flask(__name__)

def extract_lob_number(json_path):
    """Extrae el número LOB de un archivo JSON individual."""
    try:
        with open(json_path, encoding="utf-8") as f:
            card_data = json.load(f)
            for card_set in card_data.get("card_sets", []):
                if card_set.get("set_name") == "Legend of Blue Eyes White Dragon":
                    set_code = card_set.get("set_code", "")
                    match = re.search(r"LOB-(?:EN|E)?(\d+)", set_code)
                    if match:
                        return int(match.group(1))
    except Exception as e:
        print(f"Error leyendo {json_path}: {e}")
    return 9999  # Para que las cartas sin número se vayan al final

@app.route("/")
def index():
    folder = os.path.join(app.static_folder, "Legend_of_Blue_Eyes_White_Dragon")

    card_entries = []

    # Recorremos todos los archivos de la carpeta
    for file in os.listdir(folder):
        if file.endswith(".jpg"):
            base_name = os.path.splitext(file)[0]  # Quita la extensión
            json_path = os.path.join(folder, base_name + ".json")
            image_path = "Legend_of_Blue_Eyes_White_Dragon/" + file
            lob_number = extract_lob_number(json_path)
            card_entries.append((lob_number, image_path))

    # Ordenamos por el número extraído
    card_entries.sort(key=lambda x: x[0])

    # Solo las rutas de imagen ordenadas
    images_sorted = [img for _, img in card_entries]

    return render_template("index.html", images=images_sorted)

if __name__ == "__main__":
    app.run(debug=True)
