# Steam Workshop publishing kit

Everything needed for the Steam Workshop and Paradox Mods listings. Nothing here ships with the mod
itself — the mod is `descriptor.mod`, `thumbnail.png` and `gfx/` in the repository root.

| File | Where it goes |
| --- | --- |
| `description-en.txt` | Workshop item description (BBCode) |
| `description-ru.txt` | Russian version of the same description |
| `description-paradoxmods-en.txt` | same text without BBCode, for the Paradox Mods site |
| `description-paradoxmods-ru.txt` | Russian version without BBCode |
| `short-description-en.txt` | Launcher / Paradox Mods short description, under 200 chars |
| `short-description-ru.txt` | Russian short description, under 200 chars |

The `description-paradoxmods-*.txt` files are derived from the BBCode ones (headers
uppercased, `[*]` to `-`, tags dropped, `[url]` reduced to the bare link). Edit the BBCode
version first and regenerate, so the two never drift apart.

Copy a description to the clipboard (Wayland):

    wl-copy < steam-workshop/description-en.txt

## Listing metadata

* **Title:** Unit Coats of Arms Without Advanced Shaders
* **Tags:** Fixes, Graphics — same as `descriptor.mod`
* **Version:** 1.0.0, `supported_version="1.20.*"`
* **Visibility:** public

Steam's description limit is 8000 bytes; both BBCode descriptions are well under it.

## Preview image on Steam

The launcher picks up `thumbnail.png` from the mod root (next to `descriptor.mod`), which is
what `picture="thumbnail.png"` in the descriptor points at. Without that file the item shows
Steam's default placeholder; images added to the item's gallery on the website do not
replace it. After adding or changing it, re-run `install.sh` and upload again from the
launcher — that updates the existing Workshop item. Steam's limit is 1 MB.

**Do not use `[code]` in the Steam files.** Steam renders it as a full-width block, so an
identifier written mid-sentence becomes its own boxed paragraph.
