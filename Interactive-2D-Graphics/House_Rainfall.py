from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W, H = 1500, 800  
number_of_drops = 165
rain_drop_length= 70
rain_speed      = 22
rain_bend       = 0.0
brightness      = 0.0
rain_drops      = []

for i in range(number_of_drops):
    x = random.randint(-W//2, W//2)
    y = random.randint(-H//2, H//2)
    color_type = random.choice(['a', 'b'])
    rain_drops.append([x, y, color_type])

def setup_projection():
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W / 2, W / 2, -H / 2, H / 2, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def draw_points(x, y, size):
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def rectangle(x1, y1, x2, y2):
    glBegin(GL_TRIANGLES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()

def draw_background():
    # b = brightness
    global brightness
    # Sky
    glColor3f(brightness * 0.90, brightness * 0.9, brightness * 1.0)
    rectangle(-W / 2, 0, W / 2, H/2)
    # Ground
    glColor3f(0.5, 0.4, 0.1)
    rectangle(-W / 2, -H / 2, W / 2, 0)

def draw_trees():
    tree_width = W/15
    tree_height = H/4 + 20
    start = -W / 2
    while start <= (W / 2):
        glColor3f(0.0, 0.6, 0.0)

        glBegin(GL_TRIANGLES)
        glVertex2f(start, 0)
        glVertex2f(start+tree_width, 0)
        glVertex2f((start+ tree_width/2),tree_height)
        glEnd()

        start += tree_width

def draw_house():
    # House without the roof
    left_wall = -W/4
    right_wall = W/4
    house_bottom = -H/4
    house_top = 100

    glColor3f(0.98, 0.95, 0.85)
    rectangle(left_wall,house_top,right_wall,house_bottom)

    # Roof
    roof_peak_y = 250
    roof_left = left_wall - 50
    roof_right = right_wall + 50

    glColor3f(0.55, 0.05, 0.05)
    glBegin(GL_TRIANGLES)
    glVertex2f(roof_left, house_top)
    glVertex2f(roof_right, house_top)
    glVertex2f(0, roof_peak_y)
    glEnd()

    # Door
    door_right = 60
    door_left = -door_right
    door_top = 15
    door_bottom = house_bottom

    glColor3f(0.75, 0.75, 0.75)
    rectangle(door_left, door_top, door_right, door_bottom)

    # Door lock
    glColor3f(0.25, 0.25, 0.30)
    draw_points(door_right - 15,(house_bottom + door_top) / 2, 20)

    # Windows
    win_top = 0
    win_bottom = -90
    l_win_left = left_wall - door_left*2
    l_win_right = door_left*2
    r_win_left = door_right*2
    r_win_right = right_wall- door_right*2
    #glColor3f(0.65, 0.85, 0.95)
    glColor3f(0.75, 0.8, 0.85)
    # Left
    rectangle(l_win_left,win_top,l_win_right,win_bottom)
    # Right
    rectangle(r_win_left,win_top,r_win_right,win_bottom)

    # Window Grill
    mid_y = (win_bottom + win_top) / 2
    mid_x_l = (l_win_left + l_win_right) / 2
    mid_x_r = (r_win_left + r_win_right) / 2

    glColor3f(0.1, 0.1, 0.1)
    glLineWidth(3)

    glBegin(GL_LINES)
    # Left window grill
    glVertex2f(mid_x_l, win_bottom)
    glVertex2f(mid_x_l, win_top)
    glVertex2f(l_win_left, mid_y)
    glVertex2f(l_win_right, mid_y)
    # Right window grill
    glVertex2f(mid_x_r, win_bottom)
    glVertex2f(mid_x_r, win_top)
    glVertex2f(r_win_left, mid_y)
    glVertex2f(r_win_right, mid_y)
    glEnd()

def draw_rain():

    glLineWidth(0.1)
    glBegin(GL_LINES)
    for  x, y, color_type in rain_drops:
        if color_type == 'a':
            glColor3f(0.7, 0.75, 0.95)
        else:
            glColor3f(0.55, 0.5, 0.40)
            
        glVertex2f(x, y) # Point 1
        glVertex2f(x + rain_bend * 3, y -rain_drop_length) # Point 2
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    
    draw_background()
    draw_trees()
    draw_house()
    draw_rain()

    glutSwapBuffers()

def animate():
    global rain_drops

    for rain_drop in rain_drops:
        x, y, color_type = rain_drop
        x += rain_bend
        y -= rain_speed

        if y < -H/2:
            y = H/2
            x = random.randint(-W//2, W//2)

        if x < -W/2:
            x = W/2
        elif x > W/2:
            x = -W/2
        rain_drop[0] = x
        rain_drop[1] = y

    glutPostRedisplay()

def keyboard_listener(key, x, y):

    global brightness
    if key == b'w':
        brightness = min(1.0, brightness + 0.05)
        if brightness == 1.0:
            print("Day time.")
        else:
            print("Getting towards morning.")
    elif key == b's':
        brightness = max(0.0, brightness - 0.05)
        if brightness == 0.0:
            print ("Night time.")
        else:
            print("Getting towards night.")
    glutPostRedisplay()

def special_key_listener(key, x, y):

    global rain_bend
    if key == GLUT_KEY_LEFT:
        rain_bend -= 0.5
        print(f"Rain is falling on the left.")
    elif key == GLUT_KEY_RIGHT:
        rain_bend += 0.5
        print(f"Rain is falling on the right.")

    glutPostRedisplay()

def main():

    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(W, H)
    glutInitWindowPosition(170, 170)
    glutCreateWindow(b"Task 1")
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)

    glutMainLoop()

if __name__ == "__main__":
    main()