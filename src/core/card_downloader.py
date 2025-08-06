import os
import requests
import json

def download_cards(pack_name):
    print(f"\n🔹 Descargando cartas del sobre: {pack_name}")

    url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
    response = requests.get(url)

    if response.status_code != 200:
        print("No se pudo obtener información de la API completa.")
        return

    data = response.json()
    cards = data["data"]
    base_folder = "C:/Users/sergi/OneDrive/Escritorio/Cartas/card_binder/static"
    pack_folder = os.path.join(base_folder, pack_name.replace(" ", "_"))
    os.makedirs(pack_folder, exist_ok=True)

    count = 0

    for card in cards:
        if "card_sets" in card and card["card_sets"] is not None:
            for set_info in card["card_sets"]:
                if set_info["set_name"] == pack_name:
                    # Normalizar nombre para archivo
                    name = card["name"].replace("/", "_").replace("\\", "_").replace(" ", "_").replace(":", "").replace("*", "")
                    card_id = card["id"]
                    image_url = card["card_images"][0]["image_url"]

                    # Archivos a guardar
                    filename_img = f"{name}_{card_id}.jpg"
                    filename_json = f"{name}_{card_id}.json"

                    filepath_img = os.path.join(pack_folder, filename_img)
                    filepath_json = os.path.join(pack_folder, filename_json)
                    
                    # Descargar imagen si no existe
                    if not os.path.exists(filepath_img):
                        try:
                            img_data = requests.get(image_url).content
                            with open(filepath_img, "wb") as f:
                                f.write(img_data)
                            print(f"Imagen guardada: {filename_img}")
                        except Exception as e:
                            print(f"Error al descargar imagen {filename_img}: {e}")
                    else:
                        print(f"Imagen ya existe: {filename_img}")

                    # Guardar info completa de la carta en JSON
                    try:
                        with open(filepath_json, "w", encoding="utf-8") as f_json:
                            json.dump(card, f_json, ensure_ascii=False, indent=4)
                        print(f"Info guardada: {filename_json}")
                    except Exception as e:
                        print(f"Error al guardar info {filename_json}: {e}")

                    count += 1
                    break  # evitar duplicados

    if count == 0:
        print(f"No se encontraron cartas para el sobre: {pack_name}")
    else:
        print(f"{count} cartas procesadas para {pack_name}")
