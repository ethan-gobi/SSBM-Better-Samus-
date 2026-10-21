# Samus Ultimate Mod for Super Smash Bros. Melee

A Samus moveset mod for **Super Smash Bros. Melee (NTSC 1.02)** that brings parts of her
*Smash Ultimate* kit into Melee: a fast, comboable zair, mid-air Charge Shot, multi-hits that
actually link, and quicker grabs. All other characters are left untouched.

This repository contains **no game files**. The installer patches a copy of an ISO you dumped from
your own disc. It writes only the mod's changes (about 2.4 KB) and checks every byte it touches.

---

## What's changed

### Zair (grab aerial)
- About 18 frames total (vanilla: 60). The hitbox comes out around frame 2.
- Samus keeps falling, drifting and can fast-fall during it. The beam moves with her.
- No free fall afterwards.
- Landing:
  - autocancels if you land before or after the hitbox is out;
  - 6 frames of landing lag if you land during it, 3 if you L-cancel.
- Weak at the cannon, strong at the tip (5%). Fixed knockback with plenty of hitstun: a combo starter, not a kill move.
- **Zair during an airdodge or from free fall** is vanilla Melee zair:
  - floaty physics, normal speed, vanilla tether, vanilla landing lag;
  - ends helpless, so it can't be used to escape free fall;
  - uses the same hitboxes as the modded zair.

### Charge Shot (neutral special)
- Can be charged in the air. You fall normally and can fast-fall while charging.
- In the air:
  - **B** fires the shot.
  - **Shield + a direction**: instant airdodge, with the charge stored (wavedash onto platforms).
  - **Shield in neutral**: plays the store-charge animation; press shield again to airdodge.
- Landing mid-charge continues the charge on the ground. Walking off a ledge mid-charge continues it in the air.
- A full charge fires straight away in the air without snapping you to the ground.

### Multi-hit moves
Multi-hits use fixed, weight-independent knockback so they link on every character at every
percent, including fast-fallers. Each move ends with a final hit that launches.

| Move | Change |
|---|---|
| Forward air | Multi-hits pull forward with Samus's drift and have bigger hitboxes; final hit 6% |
| Up air | Multi-hits link straight up; final hit 5%, launches upward |
| Up smash | Multi-hits 3/3/3/4%; final hit 9%, a strong vertical kill move |
| Screw Attack | Loop hits no longer depend on weight or percent; final hit 3% and launches (vanilla: 1%, weak). Recovery unchanged |

### Missiles
- **Homing Missile:** a little faster (speed 1.6 vs 1.3) and turns more sharply.
- **Super Missile:** accelerates sooner, top speed 2.8 (vanilla 2.2), 12% damage, slightly more knockback.

### Grabs
- Standing and dash grab are about 1.3× faster across the whole move. Same range.

---

## Installation

### What you need
1. **Your own Super Smash Bros. Melee NTSC v1.02 ISO** (game ID `GALE01`, revision 2), dumped from
   a disc you own. This is the version Dolphin and Slippi players use.
   - It must be **unmodified**. Don't use 20XX, UnclePunch, Sigma or other modded ISOs.
   - If your dump is `.nkit.iso`, `.rvz`, `.ciso` or `.gcz`, convert it to a plain `.iso` first:
     in **Dolphin**, right-click the game → **Convert File…** → Format: **ISO** → **Convert**.
2. **Python 3.8 or newer**: <https://www.python.org/downloads/>
   (Windows: tick **"Add python.exe to PATH"** in the installer.)
3. **Dolphin** (or Slippi Dolphin) to play: <https://dolphin-emu.org/download/>

### Steps
1. Download this mod: the green **Code** button → **Download ZIP**, then extract it.
   Or clone it: `git clone <this repo's URL>`.
2. Open a terminal in the extracted folder:
   - **Windows:** open the folder in File Explorer, click the address bar, type `cmd`, press Enter.
   - **macOS / Linux:** open Terminal and `cd` into the folder.
3. Run the installer, giving your ISO and a name for the new one:

   ```
   python install_samus_mod.py "C:\Games\Melee.iso" "C:\Games\Melee - Samus Mod.iso"
   ```

   On macOS/Linux use `python3` and normal paths, e.g.
   `python3 install_samus_mod.py ~/Games/Melee.iso ~/Games/Melee-SamusMod.iso`.

4. You should see:

   ```
   Input ISO verified: clean NTSC Melee 1.02.
     patched Start.dol (12 changes) - verified
     patched PlSs.dat (32 changes) - verified
   Done! Open the new ISO in Dolphin and pick Samus.
   ```

5. In Dolphin, add the folder containing the new ISO (**Config → Paths**) or just open the file,
   then play as Samus.

Your original ISO is never modified. To uninstall, delete the new ISO.

### Troubleshooting
| Message | Fix |
|---|---|
| `Game ID is ...` / `revision 1.00/1.01` | You need NTSC-U Melee **1.02**. PAL and older revisions aren't supported. |
| `... is not vanilla Melee 1.02 (it has other mods)` | Use a clean, unmodified dump. |
| `already has the Samus mod installed` | That ISO is already patched; just play it. |
| `looks like a compressed/NKit image` | Convert to plain ISO in Dolphin (see above). |
| `python` not found | Reinstall Python with "Add to PATH", or use `py` instead of `python` on Windows. |

---

## Compatibility notes
- **Online/Slippi:** only play with people running the exact same patched ISO. It will desync against
  vanilla, and it isn't allowed in Slippi ranked/unranked matchmaking. Direct connect with friends who
  installed the same mod works like any other mod.
- The mod uses the **frame-speed (FSM) engine by Magus420**, as installed by Crazy Hand, and a small amount of
  custom code. Other DOL mods or Gecko codes that use the same memory may conflict. Don't add more FSM entries
  with Crazy Hand on top of this mod.
- A couple of tiny routines live in memory that held text for Melee's internal crash/debug screen. Normal play
  never reads that text.

## Credits
- **Magus420**: Frame Speed Modifier engine.
- **Crazy Hand** (Melee character editor), used during development.
- Not affiliated with Nintendo or HAL Laboratory. Super Smash Bros. Melee is © Nintendo / HAL Laboratory.
  You must own the game to use this mod.

## License
The installer script and patch data in this repository are released under the MIT License (see `LICENSE`).
No Nintendo files are included or distributed.
