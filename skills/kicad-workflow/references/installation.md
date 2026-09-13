# Installation discovery and API compatibility

Use exhaustive discovery when the user requests the newest local version, the recorded installation fails, or the required capability is unavailable. Check all KiCad installations on `PATH`, system installation locations, and system/user package managers. For an exhaustive local search, search the home directory recursively for AppImages and portable installations, including hidden and ignored folders, within permitted filesystem access. On Linux:

```bash
rg --files --hidden --no-ignore \
  --iglob '*kicad*.appimage' --iglob 'kicad-cli' "$HOME"
```

Check user-supplied paths and known symlinked installation directories too. Query each distinct installation's actual version using its CLI or supported launcher; do not infer it from filenames. Compare versions numerically, including prerelease ordering. Use the newest compatible local version when that is the requested goal; otherwise preserve the project version. Report discovery or launch failures instead of silently falling back to an older version.

Record the verified executable or AppImage path, actual version, launch method, library paths, and Python environment in the project's existing environment notes. Reuse that record during the task; repeat discovery if it becomes stale, fails, or the user requests a different installation. Check existing installations before downloading another KiCad installation. Respect an explicit user-selected version.

Use subcommand-specific `--help` before relying on syntax that may differ between KiCad versions.

For new PCB automation, prefer KiCad's official IPC API through the `kicad-python` package, imported as `kipy`. Do not start new work on the deprecated SWIG `pcbnew` Python bindings unless an existing project already depends on them and migrating is outside the task.

Detect whether the installed version supports the required IPC operations and whether they need a running PCB Editor or offer a headless launch path. Consult that version's help and official API documentation rather than assuming capabilities from a different release.

If a useful Python package is missing, first look for the project's documented environment, lockfile, requirements, or setup scripts. Add dependencies to a project environment only when appropriate, and make the dependency reproducible rather than relying on an unexplained global install.
