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

1. Add or update mods in `mods/` and configs in `configs/`
2. Run `python compile.py` locally to verify the zip is generated in `build/`
3. Push your changes and create a GitHub release; the workflow will zip and attach the artifact automatically.

See [Dimension‑Gateway repository](https://github.com/TeamDimensional/Dimension-Gateway) for a working example.
