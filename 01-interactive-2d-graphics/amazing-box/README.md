# 📦 Amazing Box

<p align="center">
  <img src="media/amazing_box_demo.gif" alt="Amazing Box demo" width="85%">
</p>

<p align="center">🎥 <a href="media/amazing_box_demo.mp4"><b>Watch the full demo video</b></a></p>

An interactive particle box. Every right-click spawns a point with a random colour that moves diagonally and bounces off the walls. You can speed the points up or slow them down, make them blink, or freeze the whole scene. All of these work independently and in any combination.

← [Back to Interactive 2D Graphics](../) · [Back to all projects](../../)

---

## ✨ Features

- **Spawn points** exactly where you right-click, each with a random colour and a random diagonal direction (↗ ↖ ↙ ↘)
- **Wall bouncing**: a point reverses its direction when it reaches the edge of the box
- **Speed control**: speed up or slow down all points at once
- **Blink mode**: points disappear and reappear once every second
- **Freeze**: stops all movement and disables every other control until unfrozen

## 🎮 Controls

| Input | Action |
|-------|--------|
| 🖱️ Right click | Create a new point at the cursor |
| 🖱️ Left click | Toggle blinking on / off |
| `↑` Up arrow | Increase the speed of all points (×1.5) |
| `↓` Down arrow | Decrease the speed of all points (÷1.5) |
| `Space` | Freeze / unfreeze the simulation |

## 🧠 How it works

| Part | Implementation |
|------|----------------|
| Point data | Each point is stored as `[x, y, dx, dy, r, g, b]`, with `dx, dy ∈ {−1, +1}` |
| Mouse → world | `convert_coordinate()` maps window pixels to the centred orthographic coordinates |
| Movement | Every frame: `x += dx · speed`, `y += dy · speed` |
| Bouncing | Hitting a vertical wall flips `dx`; hitting a horizontal wall flips `dy` |
| Blinking | A `threading.Timer` toggles a full-screen black cover every second |
| Freeze | A single `frozen` flag stops animation and ignores input |

## ▶️ Run

```bash
python amazing_box.py
```
