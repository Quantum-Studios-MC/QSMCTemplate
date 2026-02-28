import os
import zipfile

def zip_modpack(source_dir, output_filename):
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    source_directory = "mods"
    output_zip = "build/modpack-latest.zip"

    if not os.path.exists("build"):
        os.makedirs("build")

    zip_modpack(source_directory, output_zip)
    print(f"Modpack zipped successfully: {output_zip}")