from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import os

W, H = 600, 800

score     = 0
game_over = False
paused    = False
cheat_mode= False

catcher_x = 0
catcher_y = - H//2 + 10
catcher_width  = 120
catcher_height = 20

catcher_speed = 20      
catcher_vel   = 500        
catcher_color = (1.0, 1.0, 1.0) 

diamond_size = 15
diamond_x    = random.randint(-W//2 + diamond_size, W//2 - diamond_size)
diamond_y    = H//2 - 100    
diamond_vel  = 150        
diamond_color= (1.0, 1.0, 1.0)

last_time = time.time()


def setup_projection():
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-W/2, W/2, -H/2, H/2, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def convert_coordinate(x, y):
    x = x - W/2
    y = H/2 - y
    return x, y

def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            return 0
        elif dx < 0 and dy >= 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        else:
            return 7
    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6

def toZone0(x, y, zone):
    if zone == 0: 
        return x, y
    elif zone == 1: 
        return y, x
    elif zone == 2: 
        return y, -x
    elif zone == 3: 
        return -x, y
    elif zone == 4: 
        return -x, -y
    elif zone == 5: 
        return -y, -x
    elif zone == 6: 
        return -y, x
    elif zone == 7: 
        return x, -y

def fromZone0(x, y, zone):
    if zone == 0: 
        return x, y
    elif zone == 1: 
        return y, x
    elif zone == 2: 
        return -y, x
    elif zone == 3: 
        return -x, y
    elif zone == 4: 
        return -x, -y
    elif zone == 5: 
        return -y, -x
    elif zone == 6: 
        return y, -x
    elif zone == 7: 
        return x, -y

def midpointLine(x1, y1, x2, y2):
    zone = findZone(x1, y1, x2, y2)
    
    x1_0, y1_0 = toZone0(x1, y1, zone)
    x2_0, y2_0 = toZone0(x2, y2, zone)

    if x1_0 > x2_0:
        x1_0, x2_0 = x2_0, x1_0
        y1_0, y2_0 = y2_0, y1_0

    dx = x2_0 - x1_0
    dy = y2_0 - y1_0

    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x = x1_0
    y = y1_0

    while x <= x2_0:
        px, py = fromZone0(x, y, zone)
        drawPoint(px, py)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1

def drawPoint(x, y):
    glBegin(GL_POINTS)      
    glVertex2f(x, y)        
    glEnd()

def drawCatcher():
    global catcher_x, catcher_y, catcher_width, catcher_height, catcher_color

    glColor3f(catcher_color[0], catcher_color[1], catcher_color[2])

    left   = catcher_x - catcher_width // 2
    right  = catcher_x + catcher_width // 2
    top    = catcher_y + catcher_height
    bottom = catcher_y

    midpointLine(left, top, right, top) 
    midpointLine(left, top, left + 10, bottom)
    midpointLine(left + 10, bottom, right - 10, bottom)
    midpointLine(right, top, right - 10, bottom)

def newDiamond():
    global diamond_x, diamond_y, diamond_color
    
    diamond_x = random.randint(-W//2 + diamond_size, W//2 - diamond_size)
    diamond_y = H//2 - 100 
    diamond_color = (
        random.uniform(0.6, 1.0),
        random.uniform(0.7, 1.0),
        random.uniform(0.8, 1.0)
    )

def drawDiamond():
    global diamond_x, diamond_y, diamond_size, diamond_color
    x = diamond_x
    y = diamond_y
    s = diamond_size

    glColor3f(diamond_color[0], diamond_color[1], diamond_color[2])
    
    midpointLine(x, y + s, x + s, y) 
    midpointLine(x + s, y, x, y - s) 
    midpointLine(x, y - s, x - s, y) 
    midpointLine(x - s, y, x, y + s) 

def drawRestartButton():
    glColor3f(0.0, 1.0, 1.0)
    left_x = -(W//2)+15
    top_y  = H//2 - 40
    mid_y  = H//2 - 60
    bottom_y  = H//2 - 80
    
    midpointLine(left_x + 20, top_y, left_x, mid_y)       
    midpointLine(left_x + 20, bottom_y, left_x, mid_y)       
    midpointLine(left_x, mid_y, left_x + 50, mid_y)        

def drawPlayPauseButton():
    glColor3f(1.0, 1.0, 0.0)
    top_y = H//2 - 40
    mid_y = H//2 - 60
    bottom_y = H//2 - 80

    if paused:
        midpointLine(-20, bottom_y, -20, top_y)
        midpointLine(-20, top_y, 20, mid_y)
        midpointLine(20, mid_y, -20, bottom_y)
    else:
        midpointLine(-10, bottom_y, -10, top_y)
        midpointLine(10, bottom_y, 10, top_y)

def drawExitButton():
    glColor3f(1.0, 0.0, 0.0)
    x = W//2
    top_y   = H//2 - 40
    bottom_y   = H//2 - 80

    midpointLine(x - 60, bottom_y, x - 20, top_y) 
    midpointLine(x - 60, top_y, x - 20, bottom_y) 

def checkCollision():
    global catcher_x, catcher_y, catcher_width, catcher_height, diamond_x, diamond_y, diamond_size

    catcher_left  = catcher_x - catcher_width // 2
    catcher_right = catcher_x + catcher_width // 2
    catcher_top    = catcher_y + catcher_height
    catcher_bottom = catcher_y

    diamond_left  = diamond_x - diamond_size
    diamond_right = diamond_x + diamond_size
    diamond_top   = diamond_y + diamond_size
    diamond_bottom= diamond_y - diamond_size

    if (catcher_left < diamond_right and
        catcher_right > diamond_left and
        catcher_bottom < diamond_top and
        catcher_top > diamond_bottom):
        return True
    return False

def restartGame():
    global score, game_over, paused, diamond_vel, catcher_color, last_time, cheat_mode
    score        = 0
    game_over    = False
    paused       = False
    cheat_mode   = False
    diamond_vel  = 150
    catcher_color= (1.0, 1.0, 1.0)
    last_time    = time.time() 
    newDiamond()
    print("Starting Over!")

def keyboard_listener(key, x, y):
    global cheat_mode
    if paused or game_over: 
        return
    if key == b'c':
        if cheat_mode == False:
            cheat_mode = True
        else:
            cheat_mode = False
    glutPostRedisplay()

def special_key_listener(key, x, y):
    global catcher_x
    if paused or game_over or cheat_mode: 
        return
    if key == GLUT_KEY_LEFT:
        catcher_x -= catcher_speed
        if catcher_x - catcher_width//2 < -W//2:
            catcher_x = -W//2 + catcher_width//2
            
    elif key == GLUT_KEY_RIGHT:
        catcher_x += catcher_speed
        if catcher_x + catcher_width//2 > W//2:
            catcher_x = W//2 - catcher_width//2
            
    glutPostRedisplay()

def mouse_listener(button, state, x, y):
    global paused, last_time

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x, y = convert_coordinate(x, y)

        top_bound = H//2 - 30
        bot_bound = H//2 - 90

        # Restart button 
        if -(W//2) - 10 <= x and x <= -(W//2) + 70 and bot_bound <= y and y <= top_bound:
            restartGame()

        # Play and Pause button
        elif -30 <= x and x <= 30 and bot_bound <= y and y <= top_bound:
            if paused:
                paused = False
            else:
                last_time = time.time()
                paused    = True

        # Exit button
        elif W//2 - 70 <= x and x <= W//2 - 10 and bot_bound <= y and y <= top_bound:
            print("Goodbye!")
            print("Score: ", score)
            if bool(glutLeaveMainLoop):
                glutLeaveMainLoop()
            else:
                os._exit(0)
            return

    glutPostRedisplay()
    
def animate():
    if glutGetWindow() == 0:
        return

    global last_time, diamond_y, diamond_vel, game_over, catcher_color, score, catcher_x, cheat_mode, diamond_color

    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    if not paused and not game_over:
        diamond_y -= diamond_vel * dt
        
        diamond_vel += 5 * dt

        if cheat_mode:
            if catcher_x < diamond_x:
                catcher_x += catcher_vel * dt
                if catcher_x > diamond_x:
                    catcher_x = diamond_x
            elif catcher_x > diamond_x:
                catcher_x -= catcher_vel * dt
                if catcher_x < diamond_x:
                    catcher_x = diamond_x
            
            if catcher_x - catcher_width//2 < -W//2:
                catcher_x = -W//2 + catcher_width//2
            if catcher_x + catcher_width//2 > W//2:
                catcher_x = W//2 - catcher_width//2

        if checkCollision():
            score += 1
            print("Score: ", score)
            newDiamond()
            
        elif diamond_y + diamond_size < -H//2:
            game_over = True
            catcher_color = (1.0, 0.0, 0.0)
            diamond_color = (0.0, 0.0, 0.0)
            print("Game Over!")
            print("Score: ", score)

    glutPostRedisplay()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    setup_projection()
    
    drawRestartButton()
    drawPlayPauseButton()
    drawExitButton()
    drawDiamond()
    drawCatcher()
    
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(W, H)
    glutInitWindowPosition(50,50)
    glutCreateWindow(b"Catch the Diamonds")
    
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    
    newDiamond()
    glutMainLoop()

if __name__ == "__main__":
    main()