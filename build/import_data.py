import zipfile
import json
import os
import shutil
import re
from markdownify import markdownify

from links import clear_effect_links, generate_links, generate_path

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

mappings = [
    {
        "source": "spells",
        "target": "spells-srd"
    },
    {
        "source": "conditions",
        "target": "conditionitems"
    },
    {
        "source": "feats",
        "target": "feats-srd"
    },
    {
        "source": "actions",
        "target": "actionspf2e"
    }
]


if __name__ == "__main__":
    path_zip = "F:/Foundry VTT/dev/pf2e-ru-proto/temp/json-assets.zip"

    links: dict[str,str] = {}

    for m in mappings:
        source = open_zip(path_zip, f"packs/{m["source"]}.json")
        translations = parse_json(f"F:/Foundry VTT/dev/pf2r/data/community/pf2e/packs/pf2e.{m["target"]}.json")["entries"]

        links = links | generate_links(source, translations, m["target"])
    
    clear_folder("./source/content/Состояния")
    clear_folder("./source/content/Заклинания")
    clear_folder("./source/content/Способности")
    clear_folder("./source/content/Действия")

    for m in mappings:
        source = open_zip(path_zip, f"packs/{m["source"]}.json")
        translations = parse_json(f"F:/Foundry VTT/dev/pf2r/data/community/pf2e/packs/pf2e.{m["target"]}.json")["entries"]

        for item in source:
            path = generate_path(item, translations)
            t = translations[item["name"]]

            name = t["name"] = t["name"].replace("(*)", "")
            name = name # + " / " + item["name"]
            if ":" in name:
                name = "\""+ name +"\""

            def replace_link(match:re.Match[str]):
                groups = match.groups()
                link = links[groups[0]] if groups[0] in links else groups[0]
                label = groups[1]
                return f"[[{link}|{label}]]" if label is not None else f"[[{link}]]"

            if "description" in t:
                description = clear_effect_links(t["description"])
                description = description.replace("<p></p>", "")
                description = re.sub(r"@UUID\[([^\]]+)\](?:\{([^\}]+)\})?", replace_link, description)
                description = markdownify(description)
            else:
                description = ""
            with open("./source/content/" + path + ".md", "w") as f:
                f.write("---\ntitle: "+ name + "\n---\n")

                f.write("**Источник:** " + item["system"]["publication"]["title"] + "\n\n")

                f.write("- - -\n\n")

                try:
                    f.write(description)
                except:
                    pass
        
        print(m["source"])

