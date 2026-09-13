# Saving and settings

Apply when the brief includes persistence or when changing existing saves. Preserve the platform's established storage mechanism.

* Save plain data, not engine objects: position, health, inventory, unlocked flags, seed. Include a save version integer from the first version. Write to a temporary file, flush, and rename, and keep a backup, because renames are not always atomic. Migrate old saves through an ordered chain and refuse saves from a newer version rather than corrupting them. Autosave to its own slot, on safe boundaries such as room transitions, not more than about once a minute.
* Persist settings separately from saves. Defaults should be sensible on first run without a settings file.
* Keep run state and profile state apart in games with permadeath, so dying wipes the run and not the unlocks.
