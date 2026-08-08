# 💎 Catch the Diamonds!

A simple 2D interactive game developed using **Python, PyOpenGL, GLUT, and the Midpoint Line Drawing Algorithm**.

The objective of the game is to control a catcher bowl at the bottom of the screen and catch falling diamonds. Each successfully caught diamond increases the score, while missing a diamond ends the game.

---

## 🎮 Game Overview

**Catch the Diamonds!** is a 2D arcade-style game created as part of a Computer Graphics assignment.

The project demonstrates the practical implementation of:

* Midpoint Line Drawing Algorithm
* Eight-zone line drawing
* Coordinate transformation
* AABB collision detection
* Real-time animation using delta time
* Keyboard and mouse interaction
* Game states
* Cheat Mode

The player controls a catcher at the bottom of the screen while diamonds fall from the top. The objective is to catch as many diamonds as possible. Each caught diamond increases the score, while missing a diamond ends the game.

---

## ✨ Features

### 💎 Catch Falling Diamonds

* Diamonds fall vertically from the top.
* The catcher can move horizontally.
* Each caught diamond increases the score by `1`.
* A new diamond is generated after every successful catch.
* Diamond speed gradually increases.
* The diamond's horizontal position is randomized.
* The diamond's color is randomized.

### 🔴 Game Over

When a diamond is missed:

* The game stops.
* The catcher turns red.
* The falling diamond disappears.
* The final score is printed in the console.
* The catcher can no longer be moved.

### 🔄 Restart

The **Restart** button:

* Resets the score.
* Resets the diamond speed.
* Generates a new diamond.
* Restores the catcher color.
* Starts the game again.

### ⏯️ Play / Pause

The middle button toggles between **Play** and **Pause**.

When paused:

* The diamond stops moving.
* The catcher cannot be moved.

### ❌ Exit

The Exit button:

* Prints `Goodbye!`
* Prints the final score.
* Terminates the application.

### 🤖 Cheat Mode

Press **`C`** to activate Cheat Mode.

In Cheat Mode:

* The catcher automatically moves toward the falling diamond.
* The catcher follows the diamond smoothly.
* The catcher automatically catches falling diamonds.
* Press `C` again to disable Cheat Mode.

---

# 🧠 Algorithms

## 1. Midpoint Line Drawing Algorithm

The main graphics algorithm used in this project is the **Midpoint Line Drawing Algorithm**.

Instead of using OpenGL's line primitive, the project calculates individual points and draws them using:

```python
GL_POINTS
```

### Midpoint Algorithm

For Zone 0, the algorithm calculates:

```text
dx = x2 - x1
dy = y2 - y1

d = 2 * dy - dx
incE = 2 * dy
incNE = 2 * (dy - dx)
```

The algorithm considers two possible next pixels:

```text
E  = (x + 1, y)
NE = (x + 1, y + 1)
```

The decision parameter determines which point should be selected.

If:

```text
d > 0
```

the North-East point is selected.

Otherwise, the East point is selected.

---

## 2. Eight-Zone Conversion

A line can have different slopes and directions. Instead of implementing eight different algorithms, this project uses **eight-way symmetry**.

The process is:

```text
Original Coordinates
        ↓
Find Line Zone
        ↓
Convert to Zone 0
        ↓
Run Midpoint Algorithm
        ↓
Generate Points
        ↓
Convert Back to Original Zone
        ↓
Draw Using GL_POINTS
```

### Zone Conversion Functions

The project uses:

```python
findZone()
toZone0()
fromZone0()
```

For example:

```text
Zone 0 → (x, y)
Zone 1 → (y, x)
Zone 2 → (y, -x)
Zone 3 → (-x, y)
Zone 4 → (-x, -y)
Zone 5 → (-y, -x)
Zone 6 → (-y, x)
Zone 7 → (x, -y)
```

---

# 💎 Diamond Drawing

The diamond is constructed using four midpoint lines:

```text
          (x, y+s)
             /\
            /  \
           /    \
          /      \
 (x-s,y)           (x+s,y)
          \        /
           \      /
            \    /
             \  /
              \/
          (x, y-s)
```

The implementation uses four calls to `midpointLine()` to draw the four sides of the diamond.

---

# 🥣 Catcher Drawing

The catcher is also constructed entirely using midpoint lines.

It consists of four line segments forming a bowl-like shape.

The catcher can move horizontally using the left and right arrow keys.

The program also prevents the catcher from moving outside the screen boundaries.

---

# 💥 Collision Detection

The project uses **AABB (Axis-Aligned Bounding Box)** collision detection.

The catcher and diamond are treated as rectangular bounding boxes.

A collision occurs when their bounding boxes overlap.

The collision condition used in the program is:

```python
if (catcher_left < diamond_right and
    catcher_right > diamond_left and
    catcher_bottom < diamond_top and
    catcher_top > diamond_bottom):
    return True
```

---

# ⏱️ Delta Time

The game uses delta time to make the animation independent of the computer's frame rate.

The elapsed time between frames is calculated using:

```python
current_time = time.time()
dt = current_time - last_time
```

The diamond position is then updated using:

```python
diamond_y -= diamond_vel * dt
```

This prevents the diamond's movement speed from depending directly on the frame rate.

---

# 📈 Increasing Difficulty

The diamond speed gradually increases during gameplay:

```python
diamond_vel += 5 * dt
```

Therefore, the longer the player survives, the faster the diamonds fall.

---

# 🎮 Controls

| Input            | Action             |
| ---------------- | ------------------ |
| `←` Left Arrow   | Move catcher left  |
| `→` Right Arrow  | Move catcher right |
| `C`              | Toggle Cheat Mode  |
| 🔄 Left Button   | Restart game       |
| ⏯️ Middle Button | Play / Pause       |
| ❌ Right Button   | Exit game          |

---

# 🖱️ Interface

The game contains three clickable buttons at the top of the screen.

### 🔄 Restart Button

Restarts the game and resets:

* Score
* Diamond speed
* Game state
* Catcher color

### ⏯️ Play / Pause Button

Toggles between playing and paused states.

### ❌ Exit Button

Terminates the application and prints the final score.

All three buttons are also drawn using the Midpoint Line Drawing Algorithm.

---

# 🗂️ Project Structure

```text
Catch-the-Diamonds/
│
├── Lab2(3).py
├── README.md
│
├── screenshots/
│   ├── gameplay.png
│   ├── game_over.png
│   ├── restart.png
│   └── pause.png
│
└── video/
    └── gameplay.mp4
```

---

# 🛠️ Technologies & Concepts Used

### Programming Language
- Python

### Graphics Libraries
- PyOpenGL
- OpenGL
- GLUT
- GLU

### Algorithms
- Midpoint Line Drawing Algorithm
- Eight-Zone Line Drawing
- AABB (Axis-Aligned Bounding Box) Collision Detection

### Other Concepts
- Delta Time-based Animation
- Keyboard and Mouse Event Handling
- Randomization
- Real-Time Game Loop

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/k-a-tha/Computer-Graphics-OpenGL.git
cd Computer-Graphics-OpenGL
```

## 2. Install Required Libraries

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

## 3. Run the Game

```bash
python "Catch_the_Diamonds.py"
```

---

# 📸 Screenshots

## Basic Gameplay

![Basic Gameplay](screenshots/gameplay.png)

The player controls the catcher while a diamond falls from the top.

---

## Game Over

![Game Over](screenshots/game_over.png)

When the player misses a diamond, the catcher turns red and the game stops.

---

## Restart

![Restart](screenshots/restart.png)

The restart button starts a new game and resets the score and diamond speed.

---

## Play / Pause

![Play/Pause](screenshots/pause.png)

The middle button toggles the game between playing and paused states.

---

# 🎥 Video Demonstration

## Gameplay Video

[▶️ Watch the Gameplay Demonstration](video/gameplay.mp4)

The video demonstrates:

* Normal gameplay
* Catching diamonds
* Increasing diamond speed
* Game Over
* Restart
* Play/Pause
* Exit
* Cheat Mode

---

# 🔄 Game Flow

```text
              START
                │
                ▼
       Generate New Diamond
                │
                ▼
        Diamond Starts Falling
                │
                ▼
        Move Catcher / Cheat Mode
                │
                ▼
         Check Collision
           /          \
          /            \
       Caught          Missed
         │               │
         ▼               ▼
     Score + 1        Game Over
         │
         ▼
 Generate New Diamond
         │
         └───────────────► Continue
```

---

# 🤖 Cheat Mode Flow

```text
Press C
   │
   ▼
Cheat Mode ON
   │
   ▼
Find Diamond X Position
   │
   ▼
Move Catcher Toward Diamond
   │
   ▼
Check Collision
   │
   ▼
Catch Diamond
   │
   ▼
Generate New Diamond
   │
   └──────► Continue
```

The implementation moves the catcher using a velocity and elapsed time rather than instantly placing it at the diamond's position.

---

# 🧩 Main Functions

| Function               | Purpose                                |
| ---------------------- | -------------------------------------- |
| `setup_projection()`   | Sets up the OpenGL coordinate system   |
| `convert_coordinate()` | Converts mouse coordinates             |
| `findZone()`           | Finds the zone of a line               |
| `toZone0()`            | Converts coordinates to Zone 0         |
| `fromZone0()`          | Converts coordinates back              |
| `midpointLine()`       | Implements the Midpoint Line Algorithm |
| `drawPoint()`          | Draws individual pixels                |
| `drawDiamond()`        | Draws the diamond                      |
| `drawCatcher()`        | Draws the catcher                      |
| `checkCollision()`     | Checks AABB collision                  |
| `newDiamond()`         | Creates a new random diamond           |
| `restartGame()`        | Resets the game                        |
| `animate()`            | Updates game animation                 |
| `display()`            | Displays all game objects              |
| `main()`               | Initializes and starts the application |

---

# ⚠️ Important Note

All major visual elements are drawn using the custom Midpoint Line Drawing Algorithm and `GL_POINTS`.
