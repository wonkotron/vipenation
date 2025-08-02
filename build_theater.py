import os, shutil, argparse, winreg
from build_theater_configuration import Configuration


def get_bms_dir():
    bms_dir = None
    key_path = r"SOFTWARE\WOW6432Node\Benchmark Sims\Falcon BMS 4.38"
    value_name = "baseDir"
    
    registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    key_handle = winreg.OpenKey(registry, key_path)
    if not key_handle:
        print("[ERROR] get_bms_dir():  could not open registry key")
        return None
    else:
        bms_dir, _ = winreg.QueryValueEx(key_handle, value_name)

    return bms_dir


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="build_theater",
        description="builds and packages a theater modification"
    )

    parser.add_argument("-n", "--name", help="package name")
    parser.add_argument("-v", "--version", help="version number")
    parser.add_argument("-b", "--build", help="build path")
    parser.add_argument("-m", "--mod", help="modified theater's root directory path")
    parser.add_argument("-s", "--source", help="source theater's root directory path")
    parser.add_argument("-c", "--config", help="config json path")
    parser.add_argument("-a", "--artifacts", help="build artifacts path", default="../artifacts")

    arguments = parser.parse_args()
    return arguments


def copy_from_source(source_path, build_dir, include_dirs):  
    for entry in include_dirs.entries:
        target_path = "{0}/{1}".format(source_path, entry.path)
        destination_path = "{0}/{1}".format(build_dir, entry.path)
        shutil.copytree(target_path, destination_path, ignore=shutil.ignore_patterns(*entry.exclude), dirs_exist_ok=True) 


def copy_from_mod(mod_path, build_dir):
    shutil.copytree(mod_path, build_dir)


def build_artifacts(zip_path, build_path, package_name):
    print("Build Artifacts:\t{0}".format(zip_path))
    p = os.path.abspath("{0}/{1}".format(build_path, package_name))
    shutil.make_archive(zip_path, format="zip", root_dir=build_path)


def cleanup(build_dir):
    print("Removing working directories")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)


def main():
    bms_dir = get_bms_dir()
    if bms_dir is None:
        print("[ERROR] main():  could not query bms install directory")
        return

    arguments = parse_arguments()
    config = Configuration(arguments.config)

    source_dir = "{0}/{1}".format(bms_dir, arguments.source)
    if not os.path.exists(source_dir):
        print("[ERROR] main():  source does not exist ({0})".format(source_dir))
        return

    add_on_name = "Add-On {0}".format(arguments.name)
    build_dir = "{0}/{1}".format(arguments.build, add_on_name)
    zip_path = os.path.abspath("{0}/{1} v{2}".format(arguments.artifacts, arguments.name, arguments.version))

    cleanup(arguments.build)
    copy_from_mod(arguments.mod, build_dir)
    copy_from_source(source_dir, build_dir, config.include_dirs)
    build_artifacts(zip_path, arguments.build, add_on_name)
    cleanup(arguments.build)
    print("Done.")

# exec
main()
