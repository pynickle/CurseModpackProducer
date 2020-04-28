import argparse
import requests
from gooey import Gooey, GooeyParser
import func
import cfwidget_func
import twitch_func

@Gooey
def main():
    func.preparation()
    parser = GooeyParser()
    # parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    begin = subparsers.add_parser("begin")
    begin.add_argument("Name")
    begin.add_argument("Author")
    begin.add_argument("MCVersion")
    begin.add_argument("ModpackVersion")
    begin.set_defaults(func=func.set_modpack_info)

    sub1 = subparsers.add_parser("C1")
    sub1.set_defaults(func=cfwidget_func.analysis_file)

    sub2 = subparsers.add_parser("C2")
    sub2.set_defaults(func=cfwidget_func.zipfile_info)

    sub3 = subparsers.add_parser("C3")
    sub3.add_argument("Name")
    sub3.set_defaults(func=cfwidget_func.analysis_api_info)

    sub4 = subparsers.add_parser("T1")
    sub4.set_defaults(func=twitch_func.analysis_file)

    sub5 = subparsers.add_parser("T2")
    sub5.set_defaults(func=twitch_func.zipfile_info)

    sub6 = subparsers.add_parser("T3")
    sub6.add_argument("Name")
    sub6.set_defaults(func=twitch_func.analysis_api_info)

    args = parser.parse_args()
    if "Name" in args:
        args.func(args)
    else:
        args.func()

if __name__ == "__main__":
    main()