import os
import zipfile


def zip_directory(source_dir, arc_prefix, zipf):
    # Walk a folder and add files to the archive under arc_prefix
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # compute archive name relative to the source directory, then prepend prefix
            relpath = os.path.relpath(file_path, source_dir)
            arcname = os.path.join(arc_prefix, relpath) if arc_prefix else relpath
            zipf.write(file_path, arcname)


def build_modpack(sources, output_filename):
    # keep track of paths already added so we don't duplicate when a file
    # exists in both the root and the minecraft/ subdirectory.
    seen = set()
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for src, prefix in sources:
            if os.path.exists(src):
                for root, _, files in os.walk(src):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relpath = os.path.relpath(file_path, src)
                        arcname = os.path.join(prefix, relpath) if prefix else relpath
                        if arcname in seen:
                            continue
                        seen.add(arcname)
                        zipf.write(file_path, arcname)
            else:
                print(f"warning: source path '{src}' does not exist, skipping")


if __name__ == "__main__":
    # directories relative to the repository root
    # if you are running inside a launcher instance, the files will typically
    # live under "minecraft/"; adjust paths accordingly
    sources = [
        ("mods", "mods"),
        ("minecraft/mods", "mods"),
        ("minecraft/config", "config"),
        ("minecraft/scripts", "scripts"),
        ("minecraft/groovy", "groovy"),
    ]

    output_zip = "build/modpack-latest.zip"

    if not os.path.exists("build"):
        os.makedirs("build")

    build_modpack(sources, output_zip)
    print(f"Modpack zipped successfully: {output_zip}")