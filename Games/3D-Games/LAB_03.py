from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Window
W, H = 1000, 800

# Grid
GRID_LENGTH = 500
GRID_TILES  = 10 #Tiles count 
WALL_HEIGHT = 100

# Camera 
cam_x = 0
cam_y = 600
cam_z = 600
camera_pos = (cam_x, cam_y, cam_z)
fovY  = 120

first_person_view = False 
cheat_view        = False

camera_frozen      = False             
frozen_eye_position= [0.0, 0.0, 0.0]
frozen_camera_angle= 0.0

# Player
player_x = 0.0
player_y = 0.0
player_z = 0.0
player_angle = 0.0
player_speed = 10.0 
player_rotation_speed = 5.0 

# Enemies
scale       = 1.0 
enemies     = [] 
enemy_count = 5
pulse_time  = 0.0

enemy_speed = 20.0

# Bullets
shots          = []
last_shot_time = 0.0
shot_speed     = 300.0
cooldown       = 0.5
gun_front      = [30.0, 15.0, 80.0]

# Game state                  
player_hp      = 5     
score          = 0
bullets_missed = 0 
game_over      = False 
miss_capacity  = 10 

# Cheat
cheat_mode     = False
cheat_interval = 0.7

# Time
last_frame_time = time.time()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):

    glColor3f(1.0, 1.0, 1.0)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, W, 0, H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)

    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    tile_size = (GRID_LENGTH * 2) / GRID_TILES

    glBegin(GL_QUADS)

    for i in range(GRID_TILES):
        for j in range(GRID_TILES):

            if i % 2 == j % 2 :
                glColor3f(1.0, 1.0, 1.0)
            else:
                glColor3f(0.7, 0.5, 0.9)

            x1 = -GRID_LENGTH + i * tile_size
            x2 = x1 + tile_size
            y1 = -GRID_LENGTH + j * tile_size
            y2 = y1 + tile_size

            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)

    glEnd()

def draw_boundaries():
    glBegin(GL_QUADS)

    # Above wall
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, WALL_HEIGHT)

    # Bottom wall
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, WALL_HEIGHT)

    # Right wall
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, WALL_HEIGHT)

    # Left wall
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, WALL_HEIGHT)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, WALL_HEIGHT)

    glEnd()

def draw_player():
    glPushMatrix()
    glTranslatef(player_x, player_y, player_z)
    
    if game_over:
        glTranslatef(0, 0, 5)
        glRotatef(90, 1, 0, 0)
        
    glRotatef(player_angle, 0, 0, 1)
    glTranslatef(-15, 0, 0)
    # right leg
    glPushMatrix()
    glColor3f(0, 0, 1)
    gluCylinder(gluNewQuadric(), 5, 10, 50, 10, 10)
    glPopMatrix()

    # left leg
    glPushMatrix()
    glTranslatef(30, 0, 0)
    glColor3f(0, 0, 1)
    gluCylinder(gluNewQuadric(), 5, 10, 50, 10, 10)
    glPopMatrix()

    # body 
    glPushMatrix()
    glTranslatef(15, 0, 70)
    glColor3f(0.0, 1.0, 0.0)
    glutSolidCube(40)
    glPopMatrix()

    # head sphere 
    glPushMatrix()
    glTranslatef(15, 0, 110)
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 20, 10, 10)
    glPopMatrix()

    # left arm (
    glPushMatrix()
    glTranslatef(35, -60, 80)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1.0, 1.0, 1.0)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10)
    glPopMatrix()

    # right arm 
    glPushMatrix()
    glTranslatef(-5, -60, 80)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1.0, 1.0, 1.0)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(15, -60, 80)
    glTranslatef(0, -40, 0)         
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.1, 0.2, 0.3)
    gluCylinder(gluNewQuadric(), 1, 10, 80, 10, 10)
    glPopMatrix()

    glPopMatrix()

def draw_bullets(b):
    glColor3f(0.0, 0.0, 0.0)

    glPushMatrix()

    glTranslatef(b["x"], b["y"], b["z"])
    glRotatef(-90, 1,0,0)
    glutSolidCube(10)

    glPopMatrix()

def shoot():
    global last_shot_time, shots, first_person_view

    current_time = time.time()
    if current_time - last_shot_time < cooldown: 
        return
    last_shot_time = current_time

    # According to the gun
    gun_off_x = gun_front[0]
    gun_off_y = gun_front[1]
    gun_off_z = gun_front[2]

    if first_person_view:
        r = math.radians(player_angle + 45.0)
        sx = player_x + gun_off_x * math.sin(r) - gun_off_y * math.cos(r)
        sy = player_y - gun_off_x * math.cos(r) - gun_off_y * math.sin(r)
        sz = player_z + gun_off_z
    else:
        r = math.radians(player_angle - 90.0)
        offx = gun_off_x * math.cos(r) - gun_off_y * math.sin(r)
        offy = gun_off_x * math.sin(r) + gun_off_y * math.cos(r)
        sx = player_x + offx
        sy = player_y + offy
        sz = player_z + gun_off_z

    travel_angle = math.radians(player_angle - 90.0)
    dx = math.cos(travel_angle)
    dy = math.sin(travel_angle)

    shots.append({
        "x": sx, 
        "y": sy, 
        "z": sz, 
        "dx": dx, 
        "dy": dy
    })

def draw_enemies(i): 

    glPushMatrix()
    glTranslatef(i[0], i[1], i[2]+40.0)

    # Body
    glColor3f(1.0, 0.0, 0.0)
    gluSphere(gluNewQuadric(), 35.0 * scale, 20, 20)

    # Head
    glColor3f(0.0, 0.0, 0.0)
    glTranslatef(0, 0, 50.0)
    gluSphere(gluNewQuadric(), 15.0 * scale, 20, 20)

    glPopMatrix()

def enemy():
    global enemies
    count = 0
    while count < enemy_count:
        x = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)
        y = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)

        while abs(x) < 200:
            x = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)

        while abs(y) < 200:
            y = random.uniform(-GRID_LENGTH + 100, GRID_LENGTH - 100)

        enemies.append([x,y,0])
        count += 1

def cheat(dt):
    global player_angle, last_shot_time
    
    if len(enemies) == 0:
        return

    player_angle = (player_angle + player_rotation_speed / 10.0) % 360.0

    for e in enemies:
        dx = player_x - e[0]
        dy = player_y - e[1]
        
        target_angel = (math.degrees(math.atan2(dy, dx)) - 90.0) % 360.0
        diff = abs((player_angle - target_angel + 540.0) % 360.0 - 180.0)
        
        if diff < 2.0:  
            current_time = time.time()
            if current_time - last_shot_time > cheat_interval:
                shoot()
            break

def setupCamera():

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if first_person_view:
        if cheat_mode and not cheat_view:
            r = math.radians(frozen_camera_angle)

            eye_x = player_x
            eye_y = player_y
            eye_z = player_z + 135.0

            tx = eye_x + math.sin(r) * 100.0
            ty = eye_y - math.cos(r) * 100.0
            tz = eye_z

            gluLookAt(eye_x, eye_y, eye_z,
                    tx, ty, tz,
                    0, 0, 1)

        else:
            r = math.radians(player_angle)

            eye_x = player_x
            eye_y = player_y
            eye_z = player_z + 135.0

            tx = eye_x + math.sin(r) * 100.0
            ty = eye_y - math.cos(r) * 100.0
            tz = eye_z

            gluLookAt(eye_x, eye_y, eye_z,
                    tx, ty, tz,
                    0, 0, 1)

    else:
        x, y, z = camera_pos
        res     = math.radians(x)
        cama_x  = y * math.sin(res)
        cama_y  = y * math.cos(res)
        cama_z  = z
        gluLookAt(cama_x, cama_y, cama_z,
                   0, 0, 0, 
                   0, 0, 1)
        
def keyboardListener(key, x, y):
    global player_x, player_y, player_z, player_angle, player_hp, score, bullets_missed, game_over, cheat_mode, first_person_view, cheat_view, camera_frozen, shots, enemies, enemy_count, player_rotation_speed,  frozen_camera_angle

    # Restart Game (R)
    if key == b'r' or key == b'R':      
        player_hp = 5
        score = 0
        bullets_missed = 0
        game_over = False

        cheat_mode = False
        cheat_view = False
        camera_frozen = False
        first_person_view = False
        frozen_eye_position[:] = [0.0, 0.0, 0.0]
        player_x = 0.0
        player_y = 0.0
        player_z = 0.0
        player_angle = 0.0  
        
        player_rotation_speed = 5.0
        shots.clear()
        enemies.clear()
        enemy_count = 5
        enemy()
        return

    if game_over:
        return
    x = player_x
    y = player_y
    z = player_z
    # Cheat mode (C)
    if key == b'c' or key == b'C':

        cheat_mode = not cheat_mode

        if cheat_mode:

            frozen_eye_position[0] = player_x
            frozen_eye_position[1] = player_y
            frozen_eye_position[2] = player_z + 135.0
            frozen_camera_angle = player_angle
            camera_frozen = True
            cheat_view = False

        else:
            camera_frozen = False
            cheat_view = False
    # V
    if key == b'v' or key == b'V':
        
        if first_person_view and cheat_mode:
            cheat_view = not cheat_view
            
    # W - Move Forward
    if key == b'w' or key == b'W':
        x -= player_speed * math.sin(math.radians(-player_angle))
        y -= player_speed * math.cos(math.radians(player_angle))
        x = max(-GRID_LENGTH, min(GRID_LENGTH, x))
        y = max(-GRID_LENGTH, min(GRID_LENGTH, y))

    # S - Move Backward
    elif key == b's' or key == b'S':
        x += player_speed * math.sin(math.radians(-player_angle))
        y += player_speed * math.cos(math.radians(player_angle))
        x = max(-GRID_LENGTH, min(GRID_LENGTH, x))
        y = max(-GRID_LENGTH, min(GRID_LENGTH, y))

    # A
    elif key == b'a' or key == b'A':
        player_angle = (player_angle + player_rotation_speed) % 360.0

        if first_person_view and cheat_mode and not cheat_view:
            frozen_camera_angle = player_angle

    # D
    elif key == b'd' or key == b'D':
        player_angle = (player_angle - player_rotation_speed) % 360.0

        if first_person_view and cheat_mode and not cheat_view:
            frozen_camera_angle = player_angle
            
    player_x = x
    player_y = y
    player_z = z

def specialKeyListener(key, x, y):
    global camera_pos, cam_x, cam_y, cam_z

    # Move camera up
    if key == GLUT_KEY_UP:
        cam_z -= 10
        cam_y -= 10
    # Move camera down
    if key == GLUT_KEY_DOWN:
        cam_z += 10
        cam_y += 10
    # Move camera left
    if key == GLUT_KEY_LEFT:
        cam_x -= 5
    # Move camera right
    if key == GLUT_KEY_RIGHT:
        cam_x += 5

    camera_pos = (cam_x, cam_y, cam_z)

def mouseListener(button, state, x, y):
    global first_person_view, player_rotation_speed, game_over,  frozen_camera_angle

    if state != GLUT_DOWN or game_over:
        return

    # Shoot
    if button == GLUT_LEFT_BUTTON:
        shoot()
    # First-person view 
    elif button == GLUT_RIGHT_BUTTON:

        first_person_view = not first_person_view

        if first_person_view and cheat_mode and not cheat_view:

            frozen_eye_position[0] = player_x
            frozen_eye_position[1] = player_y
            frozen_eye_position[2] = player_z + 135.0

        frozen_camera_angle = player_angle


def idle():
    global player_hp, game_over, enemies, shots, scale, pulse_time, enemy_count, bullets_missed, last_frame_time, enemy_speed, score, cheat_mode

    current_time = time.time()
    dt = current_time - last_frame_time
    last_frame_time = current_time
    
    if game_over:
        glutPostRedisplay()
        return
    if cheat_mode == True:
        cheat(dt)

    # Pulse Animation
    pulse_time += 0.01
    scale = 1.0 + 0.5 * math.sin(pulse_time)

    # Update Bullets Position
    remaining_shots = []
    for s in shots:
        s["x"] += s["dx"] * shot_speed * dt
        s["y"] += s["dy"] * shot_speed * dt

        if abs(s["x"]) > GRID_LENGTH or abs(s["y"]) > GRID_LENGTH:
            bullets_missed += 1
            if bullets_missed >= miss_capacity:
                game_over = True
                enemies.clear()
                shots.clear()
                glutPostRedisplay()
                return
        else:
            remaining_shots.append(s)

    shots = remaining_shots

    bullets_to_remove = []

    for bullet in shots:
        for e in enemies:
            
            dx = bullet["x"] - e[0]
            dy = bullet["y"] - e[1]
            distance = math.sqrt(dx * dx + dy * dy)

            # If bullet touches enemy
            if distance < 60:
                score += 1
                bullets_to_remove.append(bullet)
                enemies.remove(e)
                
                enemy_count = 1
                enemy()
                enemy_count = 5
                
                break  

    # Clean up the bullets
    for b in bullets_to_remove:
        if b in shots:
            shots.remove(b)

    # Enemy & Player Collision
    remaining_enemies = []
    for e in enemies:
        dx = player_x - e[0]
        dy = player_y - e[1]
        distance = math.sqrt(dx * dx + dy * dy)

        # Collision with Player
        if distance < 30:
            player_hp -= 1

            if player_hp <= 0:
                game_over = True
                enemies.clear()
                shots.clear()
                glutPostRedisplay()
                return
            
            enemy_count = 1
            enemy()
            enemy_count = 5 # Reset the count

        # No collision
        else:
            if distance > 0:
                e[0] += (dx / distance) * enemy_speed * dt
                e[1] += (dy / distance) * enemy_speed * dt
            
            remaining_enemies.append(e)

    enemies = remaining_enemies

    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0,0,W,H)

    setupCamera()
    draw_grid()
    draw_boundaries()
    draw_player()

    if game_over == False:
        for i in enemies:
            draw_enemies(i)
        for b in shots:
            draw_bullets(b)

        draw_text(10, H-20, f"Player Life Remaining: {player_hp}")
        draw_text(10, H-40, f"Game Score: {score}")
        draw_text(10, H-60, f"Player Bullet Missed: {bullets_missed}")
    else:
        draw_text(10, H-20, f"Game is Over. Your Score is: {score}.")
        draw_text(10, H-40, 'Press "R" to RESTART the Game.')
    
    glutSwapBuffers()

def main():
    glutInit()

    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(W, H)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Lab 03")
    glEnable(GL_DEPTH_TEST)
    glClearColor(0,0,0,1)
    
    enemy()

    glutDisplayFunc(showScreen) # Display
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle) # Animate 

    glutMainLoop()

if __name__ == "__main__":
    main()