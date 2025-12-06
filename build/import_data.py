import zipfile
import json
import os
import shutil
import re

def parse_json(file: str):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def open_zip(file:str, inner_path:str):
    with zipfile.ZipFile(file) as zip:
        with zip.open(inner_path) as f:
            data = json.load(f)
    return data

def clear_folder(directory_path:str):
    if not os.path.exists(directory_path):
        print(f"Directory '{directory_path}' does not exist.")
        return

    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove file or symbolic link
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove subdirectory and its contents
        except OSError as e:
            print(f"Error removing {item_path}: {e}")


if __name__ == "__main__":
    path_zip = "F:/Foundry VTT/dev/pf2e-ru-proto/temp/json-assets.zip"
    spells_source = open_zip(path_zip, "packs/spells.json")
    spells_translate = parse_json("F:/Foundry VTT/dev/pf2r/data/community/pf2e/packs/pf2e.spells-srd.json")["entries"]

    conditions_source = open_zip(path_zip, "packs/conditions.json")
    conditions_translate = parse_json("F:/Foundry VTT/dev/pf2r/data/community/pf2e/packs/pf2e.conditionitems.json")["entries"]

    
    clear_folder("./source/content/Состояния")

    for item in conditions_source:
        uuid = "Compendium.pf2e.conditionitems.Item."+item["_id"]
        t = conditions_translate[item["name"]]

        name = t["name"] = t["name"].replace("(*)", "")
        name = name + " / " + item["name"]
        if ":" in name:
            name = "\""+ name +"\""

        if "description" in t:
            description = re.sub(r"@UUID\[([^\]]+)\]", r"[[\1]]", t["description"])
        else:
            description = ""
        with open("./source/content/Состояния/" + uuid + ".md", "w") as f:
            f.write("---\ntitle: "+ name + "\n---\n")

            f.write("**Источник:** " + item["system"]["publication"]["title"] + "\n\n")

            f.write("- - -\n\n")

            try:
                f.write(description)
            except:
                pass


    clear_folder("./source/content/Заклинания")

    for item in spells_source:
        uuid = "Compendium.pf2e.spells-srd.Item."+item["_id"]
        t = spells_translate[item["name"]]

        name = t["name"] = t["name"].replace("(*)", "")
        name = name + " / " + item["name"]
        if ":" in name:
            name = "\""+ name +"\""

        if "description" in t:
            description = re.sub(r"@UUID\[([^\]]+)\]", r"[[\1]]", t["description"])
        else:
            description = ""
        with open("./source/content/Заклинания/" + uuid +".md", "w") as f:
            f.write("---\ntitle: "+ name + "\n---\n")

            f.write("**Источник:** " + item["system"]["publication"]["title"] + "\n\n")

            f.write("- - -\n\n")

            try:
                f.write(description)
            except:
                pass
