<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header&text=Pro%20Premium%20Cursors&fontSize=58&fontAlignY=35&desc=macOS%20Style%20%7C%20Fully%20Rounded%20%7C%20Beach%20Ball%20Busy&descAlignY=62" alt="Pro Premium Cursors" width="100%"/>

# 🖱️ Pro Premium Cursors

### *Your mouse, but make it premium.*

**A complete premium Windows cursor scheme — all 17 pointers, redesigned.**
**Dark navy glass fill · crisp white border · cyan glow · buttery animated spinners.**

<br/>

![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Cursors](https://img.shields.io/badge/Cursors-17%20Complete-38BDF8?style=for-the-badge)
![Version](https://img.shields.io/badge/Version-3.0.0-E11D48?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)

<br/>

[![⬇️ Download Installer](https://img.shields.io/badge/⬇️_Download-PremiumCursors--Setup.exe-3B82F6?style=for-the-badge&logo=github&logoColor=white)](https://github.com/akhilesh2412/PremiumCursors/releases/latest)
[![⭐ Star this repo](https://img.shields.io/badge/⭐_Star-this_repo-F59E0B?style=for-the-badge)](https://github.com/akhilesh2412/PremiumCursors)

</div>

---

## 👀 Preview — The Full Set

<div align="center">
<img src="assets/preview.png" alt="All 17 Pro Premium cursors" width="620"/>
</div>

Every single Windows pointer is covered — no half-done pack where half the cursors stay default:

| | | | |
| --- | --- | --- | --- |
| Normal Select | Help Select | Working in Background *(animated)* | Busy *(animated)* |
| Precision Select | Text Select | Handwriting | Unavailable |
| Vertical Resize | Horizontal Resize | Diagonal Resize 1 | Diagonal Resize 2 |
| Move | Alternate Select | Link Select | Location Select |
| Person Select | | | |

---

## ⬇️ Install — One Click

### Option 1 — EXE Installer *(recommended)*

1. Download **`PremiumCursors-Setup.exe`** from the [**Latest Release**](https://github.com/akhilesh2412/PremiumCursors/releases/latest)
2. Run it → **Install**
3. **Done — the cursors apply instantly.** No settings to open, no restart. Just move your mouse. 🖱️✨

> The installer copies the scheme to `C:\Windows\Cursors\ProPremium`, registers it as **“Pro Premium”** in *Mouse Properties → Pointers*, and activates it immediately. Uninstall any time from *Windows Settings → Apps* — the default Windows scheme is restored.

### Option 2 — Classic INF

1. Download the `cursors` folder from this repo
2. Right-click **`install.inf`** → **Install**
3. Pick **Pro Premium** in *Settings → Mouse → Additional mouse settings → Pointers*

### Option 3 — Manual

Copy the `.cur` / `.ani` files anywhere and assign them one-by-one in *Mouse Properties → Pointers → Browse*.

---

## ✨ Design — v3 macOS Style 🍎

- 🍎 **Authentic macOS look** — sleek, slim pointers, noticeably smaller and lighter than chunky Windows cursors
- 🖤 **Glossy charcoal-black fill** — a soft gradient with a top sheen, never flat black
- 🤍 **Thin white outline** — the classic Mac edge, crisp on dark *and* light backgrounds
- 🧤 **White glove Link hand** — just like macOS, with real separated fingers
- 🌈 **Spinning beach ball** — the iconic macOS **Busy** cursor, plus a mini beach ball next to the arrow for **Working in Background**
- 🎯 **Correct hotspots** — every click lands exactly where the tip points
- 🔍 **Two sizes in every file** (32px + 48px) — sharp on normal and high-DPI displays

> After install, the scheme shows up as **"macOS Style"** in Mouse settings.

---

## 🔨 Regenerate / Customize

All cursors are drawn **from code** — no binary blobs to trust, tweak the colours and rebuild:

```powershell
pip install pillow
python scripts/generate_cursors.py   # → cursors\  (15 .cur + 2 .ani)
```

Change `ACCENT`, `TOP` / `BOTTOM` in the script for your own colourway, rebuild the installer with [NSIS](https://nsis.sourceforge.io/): `makensis installer\installer.nsi`

---

## 🗂️ Project Structure

```
PremiumCursors/
├── 🖱️ cursors/               ← the 17 cursor files + install.inf
├── 📁 installer/
│   ├── installer.nsi         ← NSIS installer (installs + applies the scheme)
│   └── install.inf           ← classic right-click installer
├── 📁 scripts/
│   └── generate_cursors.py   ← draws every cursor from code (Pillow)
└── 📁 assets/
    └── preview.png           ← the full-set preview above
```

---

## 📄 License

MIT — see [`LICENSE`](LICENSE). Use it, fork it, remix your own colourway.

<div align="center">

### Made with ❤️ by [@akhilesh2412](https://github.com/akhilesh2412)

**If your mouse feels premium now, give it a ⭐**

</div>
