import argparse
import requests
from gooey import Gooey, GooeyParser
import func
import cfwidget_func
import twitch_func


@Gooey
def main():
    func.preparation()
    parser = GooeyParser(description="Curse Minecraft Modpack Producer")
    # parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    begin = subparsers.add_parser("Begin", help="Set the basic information of your modpack")
    begin.add_argument("Name", help="The name of your modpack")
    begin.add_argument("Author", help="The author of the modpack")
    begin.add_argument("MCVersion", help="The Minecraft Version of your modpack")
    begin.add_argument("ModpackVersion", help="The version of your modpack")
    begin.set_defaults(func=func.set_modpack_info)

    custom = subparsers.add_parser("Custom", help="Add project by ProjectID and FileID")
    custom.add_argument("ProjectID", type=int, help="the project id on curseforge")
    custom.add_argument("FileID", type=int, help="the file id on curseforge")
    custom.set_defaults(func=func.custom_add)

    fix = subparsers.add_parser("Fix", help="Fix some probable problem for manifest.json")
    fix.set_defaults(func=func.fix)

    sub1 = subparsers.add_parser("C1", help="The first way using cfwidget api")
    sub1.set_defaults(func=cfwidget_func.analysis_file)

    sub2 = subparsers.add_parser("C2", help="The second way using cfwidget api")
    sub2.set_defaults(func=cfwidget_func.zipfile_info)

    sub3 = subparsers.add_parser("C3")
    sub3.add_argument("Name", help="The name of the mod")
    sub3.set_defaults(func=cfwidget_func.analysis_api_info)

    sub4 = subparsers.add_parser("T1", help="The first way using twitch api")
    sub4.set_defaults(func=twitch_func.analysis_file)

    sub5 = subparsers.add_parser("T2", help="The second way using twitch api")
    sub5.set_defaults(func=twitch_func.zipfile_info)

    sub6 = subparsers.add_parser("T3")
    sub6.add_argument("Name", help="The name of the mod")
    sub6.set_defaults(func=twitch_func.analysis_api_info)

    args = parser.parse_args()
    if "Name" in args or "ProjectID" in args:
        args.func(args)
    else:
        args.func()


if __name__ == "__main__":
    main()
