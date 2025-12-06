import zipfile
import json

def parse_json(file: str):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def open_zip(file:str, inner_path:str):
    with zipfile.ZipFile(file) as zip:
        with zip.open(inner_path) as f:
            data = json.load(f)
    return data


if __name__ == "__main__":
    path_zip = "F:/Foundry VTT/dev/pf2e-ru-proto/temp/json-assets.zip"
    path_translation = "F:/Foundry VTT/dev/pf2r/data/community/pf2e/packs/pf2e.spells-srd.json"
    spells_source = open_zip(path_zip, "packs/spells.json")
    spells_translate = parse_json(path_translation)["entries"]

    for spell in spells_source:
        content = spells_translate[spell["name"]]
        name = content["name"].replace("(*)", "")
        with open("./source/content/Заклинания/" + name +".md", "w") as f:
            f.write(content["description"])
