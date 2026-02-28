# QSMC Template Modpack

This repository follows the structure of the [Dimension‑Gateway](https://github.com/TeamDimensional/Dimension-Gateway) template. It contains everything needed to build a Minecraft modpack for 1.12.2.

## Directory layout

```
.
├── .github/workflows/build.yml       # GitHub Actions workflow
├── .gitignore
├── compile.py                       # build script
├── metadata/                        # pack metadata (pack_format, description, etc.)
├── minecraft/                       # local instance (ignored by git)
├── mods/                            # your mod jars
├── configs/                         # mod config files
├── build/                           # output from compile.py
├── update.py                        # optional helper for updating mods
├── mmc-pack.json                    # MultiMC instance descriptor
└── README.md
```

## Usage

1. **Maintain a mod list, not the jars.**

   - The repository should *not* contain the `.jar` files.  Instead, keep one
     TOML metadata file for each mod under `metadata/mods/` (the pack index).
     This mirrors the approach used by Dimension‑Gateway.  Each TOML file is a
     simple description that includes the filename and a CurseForge file‑id
     (see examples in the template’s `metadata/mods` directory).
   - If you already have a Prism instance, the launcher automatically generates
     a JSON index at `minecraft/mods/.index`.  Running `update.py` now reads
     that file and creates corresponding TOML entries for any mods that
     aren’t already indexed.  You can also manually convert the file with the
     snippet below:
     ```bash
     python - <<'PY'
     import json, pathlib
     entries = json.load(open('minecraft/mods/.index'))
     for e in (entries if isinstance(entries,list) else entries.get('mods',[])):
         fname = e.get('filename') or e.get('fileName')
         if not fname: continue
         out = {
             'name': e.get('name', fname),
             'filename': fname,
         }
         cfid = e.get('curseforge_project_id') or e.get('fileID')
         if cfid:
             out['update'] = {'curseforge': {'file-id': cfid}}
         with open(f'metadata/mods/{fname}.toml','w') as f:
             for k,v in out.items():
                 if isinstance(v,dict):
                     f.write(f"\n[{k}.curseforge]\n")
                     f.write(f"file-id = {v['curseforge']['file-id']}\n")
                 else:
                     f.write(f"{k} = \"{v}\"\n")
     PY
     ```
   - The `update.py` script reads the TOML index files and downloads the
     matching jars into `minecraft/mods/` (or you can modify it to write to
     `mods/`).
   - The `.gitignore` is set up to ignore all jar files in
     `minecraft/mods/` so they are never committed; only the TOML index files
     live in the repo.

2. Add configuration files or scripts you want packaged in one of the
   following locations:
   * `minecraft/config` (or top‑level `config`)
   * `minecraft/scripts` (or top‑level `scripts`)
   * `minecraft/groovy` (or top‑level `groovy`)

3. To prepare a build locally:
   ```powershell
   py update.py      # fetch the jars listed in metadata/mods
   py compile.py     # zip mods/config/scripts/groovy into build/modpack-latest.zip
   ```
   The generated ZIP will contain whatever the update script downloaded plus any
   configuration/scripts you added.

4. Push the metadata and config changes to GitHub, then create a release.  The
   workflow defined in `.github/workflows/build.yml` will run the same two
   commands (`update.py` then `compile.py`) in the CI environment and upload
   the resulting ZIP as a release artifact.

See [Dimension‑Gateway repository](https://github.com/TeamDimensional/Dimension-Gateway) for a working example.
