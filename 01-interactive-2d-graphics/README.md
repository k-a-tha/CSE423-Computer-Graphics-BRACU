# 01 · Interactive 2D Graphics

Two interactive 2D programs that build the foundations of the course: drawing with OpenGL primitives in an orthographic view, animating every frame, and responding to the keyboard and mouse.

<table>
  <tr>
    <td width="50%" align="center">
      <a href="house-in-rainfall"><img src="house-in-rainfall/media/house_rainfall_demo.gif" alt="House in Rainfall" width="100%"></a>
      <br><b><a href="house-in-rainfall">House in Rainfall</a></b>
    </td>
    <td width="50%" align="center">
      <a href="amazing-box"><img src="amazing-box/media/amazing_box_demo.gif" alt="Amazing Box" width="100%"></a>
      <br><b><a href="amazing-box">Amazing Box</a></b>
    </td>
  </tr>
</table>

| Project | What it shows | Run |
|---------|---------------|-----|
| [**House in Rainfall**](house-in-rainfall) | A house scene built only from `GL_POINTS`, `GL_LINES` and `GL_TRIANGLES`, with falling rain you can bend left and right and a gradual day ↔ night transition. | `python house-in-rainfall/house_rainfall.py` |
| [**Amazing Box**](amazing-box) | A particle box: right-click spawns coloured points that travel diagonally and bounce off the walls; control their speed, make them blink, or freeze everything. | `python amazing-box/amazing_box.py` |

## Concepts

- Orthographic projection with `glOrtho` and a centred coordinate system
- Building shapes from primitives (`GL_POINTS`, `GL_LINES`, `GL_TRIANGLES`, `GL_QUADS`)
- Frame-by-frame animation with `glutIdleFunc`
- Keyboard, special-key and mouse callbacks
- Converting window (mouse) coordinates to world coordinates
- Boundary collision by flipping the direction of motion
