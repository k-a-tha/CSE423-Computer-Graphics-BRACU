from OpenGL.GL import *      
from OpenGL.GLUT import *    
from OpenGL.GLU import *     
import random
import threading

W, H = 1500, 800  
point_size = 15
points    = [] # [x, y, movement = dx, movement = dy, r, g, b]
speed     = 1.0            
frozen    = False          
blinking  = False # blink mode on/off
isBlinking= False # points visible/invisible
def setup_projection():
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W / 2, W / 2, -H / 2, H / 2, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

def convert_coordinate(x, y):
    a = x - (W / 2)
    b = (H / 2) - y
    return a, b

def draw_point(x, y, size, r, g, b):
    glColor3f(r, g, b)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def draw_cover():
    glColor3f(0.0, 0.0, 0.0) #Black
    glBegin(GL_QUADS)
    glVertex2d (-W/2, -H/2)
    glVertex2d (-W/2,  H/2)
    glVertex2d ( W/2,  H/2)
    glVertex2d ( W/2, -H/2)
    glEnd()

def blink():
    global isBlinking
    if blinking:
        if not frozen:
            if isBlinking == True:
                isBlinking = False
            else:
                isBlinking = True
        threading.Timer(1.0, blink).start()

def keyboard_listener(key, x, y):
    global frozen
    if key == b' ':
        if frozen == False:
            frozen = True
            print ("Frozen")
        else:
            frozen = False
            print ("Unfrozen")
    glutPostRedisplay()

def special_key_listener(key, x, y):
    global speed
    if frozen == False:
        if key == GLUT_KEY_UP:
            speed *= 1.5
            print(f"Speed increased")
        elif key == GLUT_KEY_DOWN:
            speed /= 1.5
            print(f"Speed decreased")
    glutPostRedisplay()

def mouse_listener(button, state, x, y):
    global blinking
    global isBlinking
    if frozen == False:
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            x, y = convert_coordinate(x, y)
            
            dx = random.choice([-1, 1])
            dy = random.choice([-1, 1])

            r = random.uniform(0.1, 1.0)
            g = random.uniform(0.2, 1.0)
            b = random.uniform(0.3, 1.0)
            points.append([x, y, dx, dy, r, g, b])
            print ("New point Created")

        elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

            if blinking == False:
                blinking = True
                isBlinking = False
                threading.Timer(1, blink).start()
                print("Blinking")
            else:
                blinking = False
                print("Not Blinking")
    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()

    for i in points:
        x, y, dx, dy, r, g, b = i
        draw_point(x, y, point_size, r, g, b)

    if blinking and isBlinking:
        draw_cover()

    glutSwapBuffers()

def animate():
    if not frozen:
        for point in points:
            x, y, dx, dy, r, g, b = point

            x += dx * speed
            y += dy * speed

            if x >= W/2 or x <= -W/2:
                dx *= -1

            if y >= H/2 or y <= -H/2:
                dy *= -1

            point[0] = x
            point[1] = y
            point[2] = dx
            point[3] = dy
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(W, H)
    glutInitWindowPosition(170, 170)
    glutCreateWindow(b"Amazing_Box")

    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()

if __name__ == "__main__":
    main()
