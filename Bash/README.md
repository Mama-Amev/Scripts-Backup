# 🚀 Bazzite App Installer

> **Vibecoded into existence by me and Claude. Use at your own risk. Preferably don't use it at all if you're not me.**

This script was not carefully engineered by a sober professional. It was assembled through a conversation with an AI assistant, iterated on the fly, and shaped entirely around one person's specific setup. That person is me. If you are not me, this script was not made for you, is not tested for you, and I take zero responsibility for what happens to your system if you run it.

It works on **[Bazzite](https://bazzite.gg/)**. That's it. That's the whole target. Not Fedora. Not Ubuntu. Not your cousin's Arch install. Bazzite.

---

## 🤖 What "Vibecoded" Means Here

This script was built collaboratively with **Claude (Anthropic)** through a back-and-forth conversation. The logic, structure, dependency handling, post-install report system, and inline guides were all produced iteratively — not planned upfront, not reviewed by a team, not tested in a CI pipeline. It grew organically from "install my apps" into whatever it is now.

It has been syntax-checked. It has been run. It mostly works. Beyond that, God himself would need to audit it line by line to be fully certain of its contents.

---

## 🎯 What This Actually Does

A single Bash script that runs on **Bazzite** and:

1. Checks Flatpak is available and Flathub is configured
2. Pre-installs system-level dependencies via `rpm-ostree` that various apps silently need to function
3. Installs a curated list of Flatpak apps from Flathub
4. For Windows-only or otherwise uninstallable apps, prints detailed manual instructions inline
5. Tracks every failure and every manual-action item throughout the run
6. Dumps a full **POST-INSTALL REPORT** at the end with fix commands for failures and step-by-step guides for everything that needs manual work

---

## 📦 Applications Installed

### Browsers
| App | Flatpak ID |
|-----|-----------|
| Floorp Browser | `one.ablaze.floorp` |
| Waterfox | `net.waterfox.waterfox` |
| Google Chrome | `com.google.Chrome` |

### Gaming
| App | Flatpak ID |
|-----|-----------|
| Steam | `com.valvesoftware.Steam` |
| Bottles (Wine manager) | `com.usebottles.bottles` |
| Flatseal | `com.github.tchx84.Flatseal` |

### VPN
| App | Flatpak ID | Notes |
|-----|-----------|-------|
| Surfshark VPN | `com.surfshark.Surfshark` | ⚠️ Kill Switch not in Flatpak build |

### Communication
| App | Flatpak ID |
|-----|-----------|
| Discord | `com.discordapp.Discord` |
| Vesktop | `dev.vencord.Vesktop` |

### Music
| App | Flatpak ID |
|-----|-----------|
| Spotify | `com.spotify.Client` |

### Development
| App | Flatpak ID | Notes |
|-----|-----------|-------|
| VSCodium | `com.vscodium.codium` | |
| Wireshark | `org.wireshark.Wireshark` | ⚠️ Needs group setup for live capture — automated |

### Game Launchers & Stores
| App | Flatpak ID |
|-----|-----------|
| itch.io | `io.itch.itch` |
| ATLauncher | `com.atlauncher.ATLauncher` |
| Modrinth App | `com.modrinth.ModrinthApp` |

### Mod Managers
| App | Flatpak ID |
|-----|-----------|
| r2modman | `com.github.ebkr.r2modman` |
| Limo | `io.github.limo_app.limo` |

### Hardware Monitoring
| App | Flatpak ID |
|-----|-----------|
| MangoHud Vulkan Layer | `org.freedesktop.Platform.VulkanLayer.MangoHud` |
| GOverlay | `page.codeberg.Heldek.GOverlay` |

### Screenshot & Clipping
| App | Flatpak ID |
|-----|-----------|
| Flameshot | `org.flameshot.Flameshot` |
| GPU Screen Recorder | `com.dec05eba.gpu_screen_recorder` |

---

## 🔧 System Dependencies (rpm-ostree)

These get layered at the host level. **Requires a reboot to activate.** The script queues them all at once and warns you at the end.

| Package | Why |
|---------|-----|
| `cabextract` | Wine/Bottles needs this to unpack `.cab` Windows installers |
| `p7zip` + `p7zip-plugins` | Archive extraction for Windows app installers |
| `usbutils` | USB device support for Wireshark USB capture |
| `v4l-utils` | Video device detection for GPU Screen Recorder |

### Flatpak Runtimes (for Wine/Bottles)
- `org.freedesktop.Platform//23.08`
- `org.freedesktop.Platform.Compat.i386//23.08` — 32-bit Windows app support
- `org.freedesktop.Platform.GL32.default//23.08`
- `org.freedesktop.Platform.VAAPI.Intel//23.08`
- `org.winehq.Wine.DLLs.dxvk//stable-23.08`

---

## 💀 Applications That Break / Can't Auto-Install

These are Windows-only, not on Flathub, or have platform limitations. The script handles each one by either installing the best Linux alternative or printing a full manual guide. All of this is also recapped in the post-install report.

| App | Why It Breaks | What The Script Does |
|-----|--------------|---------------------|
| **Playnite** | Windows-only .NET app | Installs Bottles; full setup guide printed at end |
| **Rockstar Games Launcher** | Windows-only, no Linux build exists | Installs Bottles; full Bottles setup guide printed at end |
| **BG3 Mod Manager** | Windows .NET 8 app, no Linux build | Installs Bottles; full .NET + Bottles guide printed at end |
| **VeraCrypt** | Not on Flathub; FUSE issues on immutable Bazzite | Full manual install guide + fuse fix printed at end |
| **Cisco Packet Tracer** | Proprietary, requires NetAcad account to download | Full manual install guide printed at end |
| **Surfshark Kill Switch** | Flatpak sandbox strips this feature out | Guide to switch to native .rpm printed at end |
| **CurseForge** | No official Linux client exists | ATLauncher installed instead (supports CurseForge packs) |
| **Vortex** | Windows-only | Limo installed instead |
| **Thunderstore App** | Overwolf-based, Windows-only | r2modman installed instead |
| **RedModManager / REDmod** | Windows-only, ships with game | r2modman handles Cyberpunk mods on Linux via Proton |
| **Medal.tv** | No Linux support, officially confirmed | GPU Screen Recorder installed instead |
| **ShareX** | Windows-only | Flameshot installed instead |
| **Borderless Gaming** | Windows-only | Gamescope (built into Bazzite) handles this natively |
| **Core Temp / HWiNFO64** | Windows-only | MangoHud + GOverlay installed instead |

---

## 📄 Post-Install Report

When the script finishes it prints a live-generated report based on what actually happened during the run:

- **Section A — Failed Installs** — Any Flatpak that errored out, with the exact retry command and common causes. Skipped entirely if everything succeeded.
- **Section B — Manual Steps Required** — Full step-by-step guides for every app that needs human action. Not "see above." Actual numbered steps with commands and download links.
- **Section C — Reboot Required** — Only fires if `rpm-ostree` changes are pending, with exactly what's waiting and what to do after.

---

## 🏃 Usage

```bash
chmod +x Installer.sh
./Installer.sh
```

Needs `sudo` for the `rpm-ostree` steps. Will ask when it gets there.

---

## ⚠️ Disclaimer

This script was made **for me, for my Bazzite setup, for my specific list of apps.** It is published here for my own version control and convenience.

If you are not me and you run this:
- It may install apps you don't want
- The `rpm-ostree` commands modify your system at the host layer and require a reboot
- Bottles permission overrides will be applied to your Flatpak environment
- Some things will probably not work exactly the same on your hardware

You have been warned. Twice now.

---

*Built for Bazzite. Vibecoded with Claude. Nobody else's problem but mine.*
