# QSMC Template Modpack

This repository contains the source for a Minecraft 1.12.2 modpack.  It uses
metadata files to describe which mods belong in the pack and a small Python
script to download them and bundle everything into a ZIP.  The workflow will
build the pack for you automatically on GitHub.



## Directory layout

```
.
├── .github/workflows/build.yml       # GitHub Actions workflow
├── README.md
├── compile.py                       # build script (packages mods/config)
├── update.py                        # downloads mods based on metadata
├── metadata/                        # TOML index files for each mod
│   └── mods/
├── minecraft/                       # local launcher instance (ignored)
├── mods/                            # optional alternate mod folder
├── build/                           # output from `compile.py`
└── mmc-pack.json                    # MultiMC/Prism instance descriptor
```

## Usage

1. **Maintain a mod list, not jar files.**

   Keep one TOML file per mod under `metadata/mods/`.  Each file looks like:

   ```toml
   name = "Example Mod"
   filename = "example-mod-1.0.jar"

   [update.curseforge]
   file-id = 1234567
   ```

   or use `update.modrinth.url = "..."` for Modrinth packages.  The
   `update.py` script reads these files and downloads missing jars into
   `minecraft/mods/` before building.

2. **Populate mod files in the instance.**

   You can either let `update.py` fetch mods automatically (see above) or
   manually drop jar files into `minecraft/mods/`.  The builder will package
   whatever is present regardless of metadata.

3. **Local build**

   ```powershell
   py update.py      # optional, downloads jars
   py compile.py     # creates build/modpack-latest.zip (contains mmc-pack.json manifest)
   ```

   Inspect the ZIP to ensure it contains a `mmc-pack.json` file and the
   `mods`, `config`, etc. subfolders.  Launchers such as Prism or MultiMC
   require the manifest in order to recognise the archive as a valid pack.

4. **Commit & push**

   ```powershell
   git add metadata/mods/*.toml compile.py update.py .github/workflows/bui
ld.yml
   git commit -m "update mods"
   git push
   ```

5. **Continuous integration**

   The workflow triggers on every `push` to `main` and can also be run
   manually.  It runs `update.py` followed by `compile.py`, then uploads the
   resulting ZIP as an artifact.  

   **Important:** GitHub's artifact service always bundles whatever you upload
   into a second ZIP file before you download it.  That means when you click
   **Artifacts → modpack** you receive a container archive that itself
   contains `modpack-latest.zip`.  You must unzip twice (or extract the
   inner file) before handing the result to your launcher.  This double‑zipping
   is a platform limitation and cannot be avoided.  That is why we also copy
   the ZIP to the GitHub release in the next step – release assets are served
   directly and are ready to import without any extra extraction.

   To avoid confusion, it’s usually easiest to download the pack from the
   **GitHub release** associated with the most recent tag; the workflow
   attaches `build/modpack-latest.zip` as an asset, and that file is
   importable straight away.
```bash
git tag v1.2.3
git push origin v1.2.3
```

When the workflow runs it will not only create the release, it’ll also attach
`build/modpack-latest.zip` as an asset.  If you push the same tag again the
`overwrite: true` option tells the action to update the existing release
instead of erroring with "already_exists".

Example snippet in your workflow:

```yaml
- name: Create GitHub release
  if: startsWith(github.ref, 'refs/tags/')
  uses: ncipollo/release-action@v1
  with:
    tag: ${{ github.ref_name }}       # drop the refs/ prefix
    name: ${{ github.ref_name }}
    token: ${{ secrets.GH_PAT }}   # <--- supply PAT here
    assets: build/modpack-latest.zip
    overwrite: true                # update the release if it already exists
```


This step is optional; you can simply download the ZIP artifact instead of
using releases.

---

See the [Dimension‑Gateway repo](https://github.com/TeamDimensional/Dimension-Gateway)
I looked at it for information. It's quite nice.
