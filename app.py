from flask import Flask, render_template, abort
import os
import json
import re

app = Flask(__name__)

def extract_lob_number(json_path):
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
    return 9999

@app.route("/")
def index():
    # Lista de sets: carpetas dentro de static/
    sets_folder = app.static_folder
    sets = [d for d in os.listdir(sets_folder) if os.path.isdir(os.path.join(sets_folder, d))]
    print(sets)
    return render_template("index.html", sets=sets)

@app.route("/set/<set_name>")
def show_set(set_name):
    set_folder = os.path.join(app.static_folder, set_name)
    if not os.path.exists(set_folder) or not os.path.isdir(set_folder):
        abort(404)

    card_entries = []
    for file in os.listdir(set_folder):
        if file.endswith(".jpg"):
            base_name = os.path.splitext(file)[0]
            json_path = os.path.join(set_folder, base_name + ".json")
            image_path = f"{set_name}/{file}"
            lob_number = extract_lob_number(json_path)
            card_entries.append((lob_number, image_path))

    card_entries.sort(key=lambda x: x[0])
    images_sorted = [img for _, img in card_entries]
    #print(images_sorted)
    return render_template("set.html", set_name=set_name, images=images_sorted)

if __name__ == "__main__":
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    app.run(debug=True)