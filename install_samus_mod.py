#!/usr/bin/env python3
"""Samus Ultimate-style moveset mod for Super Smash Bros. Melee (NTSC 1.02).

Makes a patched COPY of your own Melee ISO. Your original ISO is never modified.

Usage:
    python install_samus_mod.py "path/to/Melee.iso" "path/to/Melee - Samus Mod.iso"
"""
import hashlib
import json
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PATCH_FILE = os.path.join(HERE, "patch_data.json")


def fail(msg):
    print("\nERROR: " + msg)
    sys.exit(1)


def read_fst(f):
    """Return {filename: (offset, size, fst_entry_offset)} for every file on the disc."""
    f.seek(0x424)
    fst_off, fst_size = struct.unpack(">II", f.read(8))
    f.seek(fst_off)
    fst = f.read(fst_size)
    count = struct.unpack(">I", fst[8:12])[0]
    names = count * 12
    files = {}
    for i in range(1, count):
        e = fst[i * 12:i * 12 + 12]
        name_off = int.from_bytes(e[1:4], "big")
        name = fst[names + name_off:fst.index(b"\0", names + name_off)].decode("latin1")
        off, size = struct.unpack(">II", e[4:12])
        if not e[0]:
            files[name] = (off, size)
    return files


def locate(f):
    """Find Start.dol and PlSs.dat inside the ISO."""
    f.seek(0x420)
    dol_off = struct.unpack(">I", f.read(4))[0]
    files = read_fst(f)
    if "PlSs.dat" not in files:
        fail("PlSs.dat not found. Is this really a Melee ISO?")
    return {"Start.dol": dol_off, "PlSs.dat": files["PlSs.dat"][0]}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]
    if not os.path.isfile(src):
        fail(f"Input ISO not found: {src}")
    if os.path.abspath(src) == os.path.abspath(dst):
        fail("Output must be a different file from the input (your original stays untouched).")
    if os.path.exists(dst):
        fail(f"Output file already exists: {dst}\nDelete it or pick another name.")
    lower = src.lower()
    if lower.endswith((".nkit.iso", ".rvz", ".ciso", ".gcz", ".wbfs")):
        fail("This looks like a compressed/NKit image. Convert it to a plain .iso first "
             "(Dolphin: right-click the game > Convert File > Format: ISO).")
    with open(PATCH_FILE) as pf:
        data = json.load(pf)

    with open(src, "rb") as f:
        head = f.read(8)
        if head[:6] != b"GALE01":
            fail(f"Game ID is {head[:6]!r}; this mod needs NTSC-U Melee (GALE01).")
        if head[7] != 2:
            fail(f"This is Melee revision 1.0{head[7]}; the mod needs v1.02 (the version Slippi/Dolphin players use).")
        where = locate(f)
        for name, info in data.items():
            f.seek(where[name])
            blob = f.read(info["size"])
            h = hashlib.sha1(blob).hexdigest()
            if h == info["sha1_patched"]:
                fail("This ISO already has the Samus mod installed.")
            if h != info["sha1_vanilla"]:
                fail(f"{name} in this ISO is not vanilla Melee 1.02 (it has other mods). "
                     "Use a clean, unmodified Melee 1.02 ISO.")

    print("Input ISO verified: clean NTSC Melee 1.02.")
    print(f"Copying to {dst} (1.4 GB, this can take a minute)...")
    shutil.copyfile(src, dst)

    with open(dst, "r+b") as f:
        for name, info in data.items():
            base = where[name]
            for off, hexbytes in info["patches"]:
                f.seek(base + off)
                f.write(bytes.fromhex(hexbytes))
            f.seek(base)
            if hashlib.sha1(f.read(info["size"])).hexdigest() != info["sha1_patched"]:
                f.close()
                os.remove(dst)
                fail(f"Verification of {name} failed after patching; output deleted.")
            print(f"  patched {name} ({len(info['patches'])} changes) - verified")

    print("\nDone! Open the new ISO in Dolphin and pick Samus.")


if __name__ == "__main__":
    main()
