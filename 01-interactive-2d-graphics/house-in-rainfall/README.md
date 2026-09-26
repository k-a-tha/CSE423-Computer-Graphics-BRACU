# 🏠 House in Rainfall

<p align="center">
  <img src="media/house_rainfall_demo.gif" alt="House in Rainfall demo" width="85%">
</p>

<p align="center">🎥 <a href="media/house_rainfall_demo.mp4"><b>Watch the full demo video</b></a></p>

A 2D scene of a house surrounded by trees in steady rainfall. You can steer the rain left or right and slowly turn night into day, or day back into night. Everything is drawn using only three OpenGL primitives: **`GL_POINTS`**, **`GL_LINES`** and **`GL_TRIANGLES`**.

← [Back to Interactive 2D Graphics](../) · [Back to all projects](../../)

---

## ✨ Features

- **House** built from triangles: walls, roof, door, windows, window grills (lines) and a door lock (a large point)
- **Row of trees** generated in a loop across the whole width
- **165 animated raindrops**, each a line segment that falls every frame and wraps back to the top
- **Rain bending**: the arrow keys gradually tilt the rain direction
- **Day ↔ night**: the sky brightness changes step by step between dark and light
- Two raindrop colours so the rain stays visible on both the night and day sky

## 🎮 Controls

| Key | Action |
|-----|--------|
| `←` Left arrow | Bend the rain further to the left |
| `→` Right arrow | Bend the rain further to the right |
| `W` | Brighten the sky toward day |
| `S` | Darken the sky toward night |

## 🧠 How it works

| Part | Implementation |
|------|----------------|
| Projection | `glOrtho(-W/2, W/2, -H/2, H/2, 0, 1)` puts the origin at the centre of the window |
| Rectangles | A helper draws each rectangle as two `GL_TRIANGLES` |
| Rain | Each drop is `[x, y, colour]`; its line runs from `(x, y)` to `(x + bend·3, y − length)` |
| Animation | `animate()` moves every drop down by `rain_speed` and sideways by `rain_bend`, respawning drops that leave the screen |
| Day / night | The sky colour is multiplied by a `brightness` value in `[0, 1]` changed by `W` / `S` |

## ▶️ Run

```bash
python house_rainfall.py
```
