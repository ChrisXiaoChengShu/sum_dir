import argparse
import math
import os

SIZE_UNIT_CHOICE = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")

def func(args):
    current_dir = os.path.abspath(os.getcwd())
    if args.file_name.startswith('/'):
        root_path = os.path.join(current_dir, args.file_name)
    else:
        root_path = os.path.relpath(args.file_name, current_dir)
    size = get_directory_size(root_path, args)
    format_output(root_path, size, args.u)

def format_output(file_path, size, unit='auto'):
    s, u = convert_size_by_name(size, unit=unit)
    s = f'{s:>8.1f}{u}  {file_path}'
    print(s)

def convert_size_by_name(size_bytes, unit='auto'):
    i = SIZE_UNIT_CHOICE.index(unit) if unit != 'auto' else int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return s, SIZE_UNIT_CHOICE[i]

def get_directory_size(directory, args, cur_deep=0):
    """Returns the `directory` size in bytes."""
    total = 0
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                file_size = entry.stat().st_size
                if args.d is None or cur_deep < args.d:
                    format_output(entry.path, file_size, args.u)
                total += file_size
            elif entry.is_dir():
                try:
                    dir_size = get_directory_size(entry.path, args, cur_deep=cur_deep+1)
                    if args.d is None or cur_deep < args.d:
                        format_output(entry.path, dir_size, args.u)
                    total += dir_size
                except FileNotFoundError:
                    pass
    except NotADirectoryError:
        return os.path.getsize(directory)
    except PermissionError:
        return 0
    return total


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name")
    parser.add_argument("-d", help="max depth", type=int)
    parser.add_argument('-u', choices=SIZE_UNIT_CHOICE + ('auto',), default='auto', help="size unit")
    args = parser.parse_args()
    func(args)