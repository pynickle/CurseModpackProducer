import zipfile
import json
import requests
import modpackinfo
import func

headers = {"Content-Type": "application/json",
           "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36"}


def analysis_content(r, filename, name):
    choice = 0
    res = r.json()
    if len(res) == 0:
        print(f"Mod {name} analysis failed!")
        # failed.append(name)
        # failedfilename.append(filename)
        return
    FileID = ""
    index = 1
    while not FileID:
        try:
            if modpackinfo.VERSION == res[choice]["gameVersionLatestFiles"][index]["gameVersion"]:
                FileID = res[choice]["gameVersionLatestFiles"][index]["projectFileId"]
            index += 1
        except Exception:
            print(f"Mod {name} analysis failed!")
            # failed.append(name)
            # failedfilename.append(filename)
            return
    ProjectID = res[choice]["id"]
    FilesInfo = {
        "projectID": ProjectID,
        "fileID": FileID,
        "required": "true"
    }
    modpackinfo.MANIFEST["files"].append(FilesInfo)
    ProjectName = res[choice]["name"]

    author = res[choice]["authors"][0]["name"]
    modshow = f'<li><a href="https://minecraft.curseforge.com/mc-mods/"{ProjectID}">{ProjectName} (by {author})</a></li>\n'
    modpackinfo.MODLIST += modshow

    modpackinfo.UNCOMPLETEMODS.remove(name)
    modpackinfo.UNCOMPLETEMODSNAME.remove(filename)

    print(f"Mod {res[choice]['name']} add successfully!")


def analysis_file():
    func.get_uncomplete_mods()
    for name, file in zip(modpackinfo.UNCOMPLETEMODS,
                          modpackinfo.UNCOMPLETEMODSNAME):
        r = requests.get(
            f"https://addons-ecs.forgesvc.net/api/v2/addon/search?gameId=432&sectionId=6&searchFilter={name}",
            headers=headers)
        if r.status_code != 200:
            print(f"Mod {name} analysis failed!")
            # modpackinfo.UNCOMPLETEMODSNAME.append(file)
            # modpackinfo.UNCOMPLETEMODS.append(name)
            continue
        analysis_content(r, file, name)
    if not modpackinfo.UNCOMPLETEMODS:
        print("All mod add successfully!")
    else:
        print("failed mods number: ", len(modpackinfo.UNCOMPLETEMODS))
        func.save_data_to_file()


def zipfile_info():
    func.get_uncomplete_mods()
    for mod, name in zip(modpackinfo.UNCOMPLETEMODS,
                         modpackinfo.UNCOMPLETEMODSNAME):
        z = zipfile.ZipFile(f"mods/{name}", "r")
        if "mcmod.info" not in z.namelist():
            print(f"Mod {mod} analysis failed!")
            # failed.append(name)
            continue
        with z.open("mcmod.info", "r") as f:
            text = str(f.read(), "utf-8").replace("\n", " ")
            try:
                content = json.loads(text)
            except Exception:
                print(f"Mod {mod} analysis failed!")
                # failed.append(name)
                continue
        try:
            infoname = content[0]["name"]
        except Exception:
            print(f"Mod {mod} analysis failed!")
            # failed.append(mod)
            continue
        webname = infoname.replace(" ", "-")
        r = requests.get(
            f"https://addons-ecs.forgesvc.net/api/v2/addon/search?gameId=432&sectionId=6&searchFilter={name}",
            headers=headers)

        if r.status_code != 200:
            print(f"Mod {mod} analysis failed!")
            # failed.append(name)
            continue

        analysis_content(r, name, mod)

    if not modpackinfo.UNCOMPLETEMODS:
        print("All mod add successfully!")
    else:
        print("Failed mods number: ", len(modpackinfo.UNCOMPLETEMODS))
        func.save_data_to_file()


def get_api_info(name):
    webname = name.replace(" ", "-")
    r = requests.get(
        f"https://addons-ecs.forgesvc.net/api/v2/addon/search?gameId=432&sectionId=6&searchFilter={webname}",
        headers=headers)
    if r.status_code != 200:
        return False
    else:
        return r.json()


def analysis_api_info(args):
    name = args.Name
    res = get_api_info(name)
    if len(res) >= 3:
        print(f'1. {res[0]["name"]}')
        print(f'2. {res[1]["name"]}')
        print(f'3. {res[2]["name"]}')
    elif len(res) == 0:
        print("Mod not find!")
        return
    else:
        index = 0
        while index < len(res):
            print(f'{index+1}. {res[index]["name"]}')
            index += 1
    # choice = input("Choose the mod you want to add or try again(q): ")
    choice = 1
    if choice == "q":
        return
    else:
        choice = int(choice) - 1
        FileID = ""
        index = 0
        while not FileID:
            try:
                if modpackinfo.VERSION == res[choice]["gameVersionLatestFiles"][index]["gameVersion"]:
                    FileID = res[choice]["gameVersionLatestFiles"][index]["projectFileId"]
                index += 1
            except Exception as e:
                print(f"Mod {name} analysis failed!")
                return
        ProjectID = res[choice]["id"]
        FilesInfo = {
            "projectID": ProjectID,
            "fileID": FileID,
            "required": "true"
        }

        modpackinfo.MANIFEST["files"].append(FilesInfo)
        ProjectName = res[choice]["name"]

        author = res[choice]["authors"][0]["name"]
        modshow = f'<li><a href="https://minecraft.curseforge.com/mc-mods/"{ProjectID}">{ProjectName} (by {author})</a></li>\n'
        modpackinfo.MODLIST += modshow

        print(f"Mod {res[choice]['name']} Add successfully!")
