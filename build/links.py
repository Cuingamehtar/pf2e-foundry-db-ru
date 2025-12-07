from typing import Literal, TypedDict
import re

class SourceEntry(TypedDict):
    _id: str
    name: str
    type: Literal["spell", "condition", "feat"]

class TranslatedEntry(TypedDict):
    name: str

entry_folders = {
    "spell": "Заклинания",
    "condition": "Состояния",
    "feat": "Способности",
    "action": "Действия"
}

def generate_path(item: SourceEntry, translations: dict[str, TranslatedEntry]):
        name = translations[item["name"]]["name"] if item["name"] in translations else item["name"]
        name = re.sub(r"\(\*\)|\?|\!|\"", "", name)
        return f"{entry_folders[item["type"]]}/{name}".replace(":", "")

def generate_links(source: list[SourceEntry], translations: dict[str, TranslatedEntry], pack_id:str):
    links: dict[str,str] = {}
    for item in source:
        uuid = f"Compendium.pf2e.{pack_id}.Item.{item["_id"]}"
        links[uuid] = generate_path(item, translations)
    return links


def clear_effect_links(s:str):
     return re.sub(r"@UUID\[[^\]]+effects[^\]]+\](?:\{([^\}]+)\})?", (lambda m: m.group(1) if m.group(1) is not None else ""), s)