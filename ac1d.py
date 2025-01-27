import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -10)

def draw_sphere(radius, slices, stacks):
    for i in range(slices):
        lat0 = math.pi * (-0.5 + float(i) / slices)
        z0 = math.sin(lat0) * radius
        zr0 = math.cos(lat0) * radius
        lat1 = math.pi * (-0.5 + float(i + 1) / slices)
        z1 = math.sin(lat1) * radius
        zr1 = math.cos(lat1) * radius

        glBegin(GL_QUAD_STRIP)
        for j in range(stacks + 1):
            lng = 2 * math.pi * float(j) / stacks
            x = math.cos(lng)
            y = math.sin(lng)

            glVertex3f(x * zr0, y * zr0, z0)
            glVertex3f(x * zr1, y * zr1, z1)
        glEnd()

def draw_pyramid():
    glBegin(GL_TRIANGLES)
    glColor3f(0.8, 0.5, 0.3)
    glVertex3f(0, 2, 0)
    glVertex3f(-1, -1, -1)
    glVertex3f(1, -1, -1)
    
    glVertex3f(0, 2, 0)
    glVertex3f(1, -1, -1)
    glVertex3f(1, -1, 1)

    glVertex3f(0, 2, 0)
    glVertex3f(1, -1, 1)
    glVertex3f(-1, -1, 1)

    glVertex3f(0, 2, 0)
    glVertex3f(-1, -1, 1)
    glVertex3f(-1, -1, -1)
    glEnd()

def draw_tiger():
    glPushMatrix()
    glTranslatef(0, 0, -10)
    glColor3f(1, 0.8, 0.1)
    glBegin(GL_QUADS)
    for i in range(4):
        glVertex3f(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
    glEnd()
    glPopMatrix()

def draw_god():
    glColor3f(1, 1, 0)
    for i in range(10):
        glPushMatrix()
        glTranslatef(math.sin(i) * 3, math.cos(i) * 3, random.uniform(-3, 3))
        draw_sphere(0.5, 10, 10)
        glPopMatrix()

def draw_clouds():
    glColor3f(1, 1, 1)
    for i in range(5):
        glPushMatrix()
        glTranslatef(random.uniform(-10, 10), random.uniform(0, 5), random.uniform(-10, -30))
        glBegin(GL_POLYGON)
        for j in range(20):
            angle = 2 * math.pi * j / 20
            glVertex3f(math.cos(angle) * 2, 0, math.sin(angle) * 2)
        glEnd()
        glPopMatrix()

def random_colors():
    return (random.random() * 0.6, random.random() * 0.6, random.random() * 0.6)

def hypnotic_colors(time):
    r = math.sin(time * 0.5) * 0.5 + 0.5
    g = math.cos(time * 0.5) * 0.5 + 0.5
    b = math.sin(time * 0.25) * 0.5 + 0.5
    return (r, g, b)

def geometric_patterns(time):
    glColor3f(0.5 + math.sin(time * 0.1) * 0.5, 0.5 + math.cos(time * 0.1) * 0.5, 1)
    glBegin(GL_LINES)
    for i in range(10):
        angle = math.radians(i * 36)
        x = math.cos(angle) * 4
        y = math.sin(angle) * 4
        glVertex3f(0, 0, 0)
        glVertex3f(x, y, 0)
    glEnd()

def render_scene(camera_z, rotation_angle, time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    # Background color shifting
    glClearColor(math.sin(time * 0.1) * 0.5 + 0.5, math.cos(time * 0.1) * 0.5 + 0.5, 0.5, 1)

    # Apply camera transformations
    glTranslatef(0.0, 0.0, camera_z)
    glRotatef(rotation_angle, 0, 1, 0)

    # Draw Pyramid
    glPushMatrix()
    glTranslatef(0, -3, -10)
    draw_pyramid()
    glPopMatrix()

    # Draw God-like spheres
    glPushMatrix()
    glTranslatef(0, 0, -10)
    draw_god()
    glPopMatrix()

    # Draw the tiger
    draw_tiger()

    # Draw clouds
    draw_clouds()

    # Draw geometric patterns
    geometric_patterns(time)

    glPopMatrix()
    pygame.display.flip()

# Continuous loop to keep the window open and running
camera_z = -15
rotation_angle = 0
time = 0

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    render_scene(camera_z, rotation_angle, time)

    # Continuously update the camera position and rotation angle
    camera_z += 0.03  # Slow movement for a relaxed effect
    rotation_angle += 0.05  # Slow rotation for smoothness
    time += 0.01  # Slow down the time progression for the scene
    
    pygame.time.wait(10)  # Small delay to avoid overloading the CPU
