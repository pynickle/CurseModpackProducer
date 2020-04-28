import modpackinfo
import os
import json


def set_modpack_info(args):
    modpackinfo.VERSION = args.MCVersion

    ModpackInfo = {
        "manifestType": "minecraftModpack",
        "manifestVersion": 1,
        "name": args.Name,
        "version": args.ModpackVersion,
        "author": args.Author,
        "overrides": "overrides"
    }
    modpackinfo.MANIFEST.update(ModpackInfo)

    print("Manifest save!")

    save_data_to_file()


def preparation():
    if os.path.exists("failed.txt"):
        get_uncomplete_mods()
        return
    for root, _, files in os.walk("mods"):
        if root != "mods":
            continue
        else:
            for file in files:
                modpackinfo.UNCOMPLETEMODSNAME.append(file)
                name = file.split("-", 1)[0].split("_")[0]
                modpackinfo.UNCOMPLETEMODS.append(name)
    with open("failed.txt", "w", encoding="utf-8") as f:
        for i, j in zip(modpackinfo.UNCOMPLETEMODS,
                        modpackinfo.UNCOMPLETEMODSNAME):
            f.write(f"{i}: {j},\n")


def get_uncomplete_mods():
    modpackinfo.UNCOMPLETEMODS = []
    modpackinfo.UNCOMPLETEMODSNAME = []
    with open("failed.txt", "r", encoding="utf-8") as f:
        for i in f.readlines():
            modpackinfo.UNCOMPLETEMODS.append(i.split(": ")[0])
            modpackinfo.UNCOMPLETEMODSNAME.append(
                i.split(": ")[1].split(",\n")[0])
    if os.path.exists("manifest.json"):
        with open("manifest.json", "r", encoding="utf-8") as f:
            modpackinfo.MANIFEST = json.load(f, encoding="utf-8")
    if os.path.exists("modlist.html"):
        with open("modlist.html", "r", encoding="utf-8") as f:
            modpackinfo.MODLIST = f.read()[:-5]

def save_data_to_file():
    with open("failed.txt", "w", encoding="utf-8") as f:
        for i, j in zip(modpackinfo.UNCOMPLETEMODS,
                        modpackinfo.UNCOMPLETEMODSNAME):
            f.write(f"{i}: {j},\n")
    with open("modlist.html", "w", encoding="utf-8") as f:
        f.write(modpackinfo.MODLIST + "</ul>")
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(modpackinfo.MANIFEST, f)
