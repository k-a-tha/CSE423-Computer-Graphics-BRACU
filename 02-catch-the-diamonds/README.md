# 💎 Catch the Diamonds!

<p align="center">
  <img src="media/catch_the_diamonds_demo.gif" alt="Catch the Diamonds demo" height="520">
</p>

A 2D arcade game where you move a bowl-shaped catcher to catch falling diamonds. Every object on screen — the diamond, the catcher and all three buttons — is drawn **pixel by pixel with the Midpoint Line Drawing Algorithm** and `GL_POINTS`, without using OpenGL's line primitive.

← [Back to all projects](../)

---

## ✨ Features

- 💎 **Falling diamonds** with a random position and colour; each catch scores **+1** and spawns a new diamond
- 📈 **Increasing difficulty**: the fall speed grows continuously the longer you survive
- 🔴 **Game over** when a diamond is missed: the catcher turns red and the final score is printed
- 🔄 **Restart**, ⏯️ **Play / Pause** and ❌ **Exit** buttons, also drawn with midpoint lines
- 🤖 **Cheat mode**: the catcher follows the diamond on its own, moving smoothly with a velocity (not teleporting)
- ⏱️ **Delta-time animation**, so movement speed does not depend on the frame rate

## 🎮 Controls

| Input | Action |
|-------|--------|
| `←` / `→` | Move the catcher left / right |
| `C` | Toggle cheat mode |
| 🖱️ Click the **cyan arrow** (top-left) | Restart the game |
| 🖱️ Click the **yellow icon** (top-centre) | Play / Pause |
| 🖱️ Click the **red ✕** (top-right) | Exit (prints `Goodbye!` and the score) |

The catcher can't move while the game is paused, after game over, or while cheat mode is on.

---

## 🧠 Algorithms

### Midpoint Line Drawing (Zone 0)

For a line in Zone 0 (slope between 0 and 1), the algorithm steps one pixel along *x* and decides between the **East** pixel `(x+1, y)` and the **North-East** pixel `(x+1, y+1)` using only integer arithmetic:

```text
dx = x2 - x1          d     = 2·dy - dx
dy = y2 - y1          incE  = 2·dy
                      incNE = 2·(dy - dx)

if d > 0:  choose NE,  d += incNE,  y += 1
else:      choose E,   d += incE
x += 1
```

### Eight-Way Symmetry

Instead of eight separate line algorithms, every line is mapped into Zone 0, drawn there, and each point is mapped back:

```text
find zone  ──►  convert endpoints to Zone 0  ──►  run midpoint algorithm
                                                          │
             draw with GL_POINTS  ◄──  convert each point back to its zone
```

| Zone | To Zone 0 | Back from Zone 0 |
|:----:|:---------:|:----------------:|
| 0 | `( x,  y)` | `( x,  y)` |
| 1 | `( y,  x)` | `( y,  x)` |
| 2 | `( y, -x)` | `(-y,  x)` |
| 3 | `(-x,  y)` | `(-x,  y)` |
| 4 | `(-x, -y)` | `(-x, -y)` |
| 5 | `(-y, -x)` | `(-y, -x)` |
| 6 | `(-y,  x)` | `( y, -x)` |
| 7 | `( x, -y)` | `( x, -y)` |

If the endpoints arrive in reverse order, they are swapped, so a line draws the same way in both directions.

### Shapes from lines

```text
        (x, y+s)                      top edge
          /\                    ┌──────────────────┐
         /  \                    \                /
 (x-s,y) \  / (x+s,y)             └──────────────┘
          \/                          catcher bowl
        (x, y-s)
        diamond: 4 lines          4 lines
```

### Collision — AABB

The catcher and the diamond are treated as axis-aligned boxes; a catch happens when they overlap:

```python
if (catcher_left < diamond_right and catcher_right > diamond_left and
        catcher_bottom < diamond_top and catcher_top > diamond_bottom):
    return True
```

### Delta time & difficulty

```python
dt = current_time - last_time
diamond_y   -= diamond_vel * dt     # movement independent of FPS
diamond_vel += 5 * dt               # speed keeps rising
```

---

## 🔄 Game Flow

```text
 START ─► new diamond ─► diamond falls ─► move catcher (or cheat mode)
                                  │
                         collision check
                          │            │
                       caught        missed
                          │            │
                     score + 1     GAME OVER (catcher turns red)
                          │
                    new diamond ─► continue
```

## 🧩 Main Functions

| Function | Purpose |
|----------|---------|
| `findZone()` | Finds which of the 8 zones a line belongs to |
| `toZone0()` / `fromZone0()` | Converts points to and from Zone 0 |
| `midpointLine()` | Midpoint line algorithm for any line |
| `drawPoint()` | Draws a single pixel with `GL_POINTS` |
| `drawDiamond()` / `drawCatcher()` | Build the shapes from midpoint lines |
| `drawRestartButton()` / `drawPlayPauseButton()` / `drawExitButton()` | Draw the on-screen buttons |
| `checkCollision()` | AABB collision between catcher and diamond |
| `newDiamond()` / `restartGame()` | Spawn a diamond / reset the game |
| `animate()` | Delta-time update, cheat mode and game logic |
| `display()` | Renders everything each frame |

## ▶️ Run

```bash
python catch_the_diamonds.py
```
