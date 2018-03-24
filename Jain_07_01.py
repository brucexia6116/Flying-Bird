#Jain, Kritika
#1001-093-381
#2017-12-06
#Assignment_07_01

from OpenGL.GL import *
from OpenGL.arrays import vbo
#from OpenGLContext.arrays import *
import OpenGL.GL.shaders as sh
import numpy as np
import pygame
from pygame.constants import *

import Jain_07_02 as shaders
import Jain_07_03 as meshs
import Jain_07_04 as linalg

BIRD_RADIUS = 5.0
BIRD_LENGTH = 20.0
BIRD_WINGSPAN = 40.0
PATH_RADIUS = 100.0
PATH_HIGHT = 50.0
FLAGPOLE_HIGTH = 150.0
FLAGPOLE_RADIUS = 2.0  # half of the specified diameter
FLAG_SIZE = 30.0

class Context(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), OPENGL|DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.eye_rotation, self.eye_hight, self.eye_radius = 0.0, 150.0, 300.0
        self.bird_angle, self.left_wing, self.right_wing, self.wing = 0.0, 0.0, 0.0, 0.0  # Bird state
        self.wing_speed, self.bird_speed = 0.1, 0.1  # Bird speed
        self.time = 0.0
        self.flag_time = 0.0  # The time experienced by the Flag
        self.flag_flying = True
        # positions and vectors for the bezier surface/the Flag
        self.a, self.da = np.array([1,0,0], np.float32), np.array([1,-1,1], np.float32)
        self.b, self.db = np.array([1,1,0], np.float32), np.array([1,1,0], np.float32)

        self.Ka, self.Kd, self.Ks = [0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5] # lighting colors
        self.Ia, self.Id, self.Is = 0.33, 0.33, 0.33  # light intensities

        pygame.display.set_caption("Bird")

        meshs.load_vbos()
        self.shaders = shaders.Shaders()

    def Render(self):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glUseProgram(self.shaders.std)
        width, height = pygame.display.get_surface().get_size()
        field_of_view, near_plain_dist, far_plain_dist, aspect = 60.0, 80.0, 500.0, width/height
        glUniformMatrix4fv(self.shaders.std_uniforms["p"], 1, GL_FALSE, linalg.perspective(field_of_view*np.pi/180, near_plain_dist, far_plain_dist, aspect))

        eye = np.array([self.eye_radius*np.cos(self.eye_rotation), self.eye_hight, self.eye_radius*np.sin(self.eye_rotation)], np.float32)
        eye_right = np.array([-np.sin(self.eye_rotation), 0, np.cos(self.eye_rotation)], np.float32)
        eye_up = np.cross(eye_right, eye)
        glUniformMatrix4fv(self.shaders.std_uniforms["v"], 1, GL_FALSE, linalg.lookAt(eye, np.zeros(3, np.float32), eye_up))
        glUniform3fv(self.shaders.std_uniforms["eye"], 1, eye)
        glUniform3f(self.shaders.std_uniforms["light"], 0, 120, 200)
        glUniform3f(self.shaders.std_uniforms["Ka"], *self.Ka)
        glUniform3f(self.shaders.std_uniforms["Kd"], *self.Kd)
        glUniform3f(self.shaders.std_uniforms["Ks"], *self.Ks)
        glUniform1f(self.shaders.std_uniforms["Ia"], self.Ia)
        glUniform1f(self.shaders.std_uniforms["Id"], self.Id)
        glUniform1f(self.shaders.std_uniforms["Is"], self.Is)

        glViewport(0, 0, width, height)

        # floor
        glUniformMatrix4fv(self.shaders.std_uniforms["m"], 1, GL_FALSE, linalg.scale(20.0))
        glUniform4f(self.shaders.std_uniforms["color"], 0.8, 0.8, 0.8, 1.0)
        meshs.static_render("Plane")

        # Bird
        bird_mat = linalg.dot([linalg.translate(PATH_RADIUS, PATH_HIGHT, 0),
                               linalg.rot(-self.bird_angle, 0,1,0)])

        # Bird body
        glUniformMatrix4fv(self.shaders.std_uniforms["m"], 1, GL_FALSE,
                           linalg.dot([linalg.rot(np.pi/2,1,0,0),
                                       linalg.scale(BIRD_RADIUS, BIRD_RADIUS, BIRD_LENGTH/2),
                                       bird_mat]))
        glUniform4f(self.shaders.std_uniforms["color"], 1,0,0,1)
        meshs.static_render("Cylinder")

        # Bird head
        glUniformMatrix4fv(self.shaders.std_uniforms["m"], 1, GL_FALSE,
                           linalg.dot([linalg.scale(BIRD_RADIUS),
                                       linalg.translate(0, 0, BIRD_LENGTH/2+BIRD_RADIUS),
                                       bird_mat]))
        glUniform4f(self.shaders.std_uniforms["color"], 0,1,0,1)
        meshs.static_render("Sphere")

        # Bird right wing
        wing_length = (BIRD_WINGSPAN-2*BIRD_RADIUS)/2
        glUniformMatrix4fv(self.shaders.std_uniforms["m"], 1, GL_FALSE,
                           linalg.dot([linalg.scale(wing_length, 0, BIRD_LENGTH/2),
                                       linalg.translate(-BIRD_RADIUS, 0, 0),
                                       linalg.rot(self.right_wing, 0, 0, 1),
                                       bird_mat]))
        glUniform4f(self.shaders.std_uniforms["color"], 0,0,1,1)
        meshs.static_render("Triangle")

        # Bird left wing
        glUniformMatrix4fv(self.shaders.std_uniforms["m"], 1, GL_FALSE,
                           linalg.dot([linalg.scale(-wing_length, 0, BIRD_LENGTH/2),
                                       linalg.translate(BIRD_RADIUS, 0, 0),
                                       linalg.rot(self.left_wing, 0, 0, 1),
                                       bird_mat]))
        glUniform4f(self.shaders.std_uniforms["color"], 0,1,1,1)
        meshs.static_render("Triangle")

        glUniformMatrix4fv(self.shaders.std_uniforms["m"], 1, GL_FALSE,
                           linalg.dot([linalg.scale(FLAGPOLE_RADIUS, FLAGPOLE_HIGTH/2, FLAGPOLE_RADIUS),
                                       linalg.translate(0, FLAGPOLE_HIGTH/2, 0)]))
        glUniform4f(self.shaders.std_uniforms["color"], 1,1,0,1)
        meshs.static_render("Cylinder")

        glUniformMatrix4fv(self.shaders.std_uniforms["m"], 1, GL_FALSE,
                           linalg.dot([linalg.rot(np.pi/2, 0, 1, 0),
                                       linalg.scale(FLAG_SIZE, FLAG_SIZE, FLAG_SIZE),
                                       linalg.translate(0, FLAGPOLE_HIGTH - FLAG_SIZE, 0)]))
        glUniform4f(self.shaders.std_uniforms["color"], 1,0,1,1)
        meshs.dynamic_render("Grid", *meshs.bezier(self.a, self.da, self.b, self.db))

        glUseProgram(0)

    def Run(self):
        while True:
            time_passed = self.clock.tick(100)

            for event in pygame.event.get():
                if event.type == QUIT:
                    meshs.delete_vbos()
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.eye_hight += 5
                    elif event.key == K_DOWN:
                        self.eye_hight -= 5
                    elif event.key == K_LEFT:
                        self.eye_rotation += 5*np.pi/180.0
                    elif event.key == K_RIGHT:
                        self.eye_rotation -= 5*np.pi/180.0
                    elif event.key == K_f:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # F
                            self.bird_speed *= 1.5
                            self.wing_speed *= 1.5
                        else:  # f
                            self.bird_speed /= 1.5
                            self.wing_speed /= 1.5
                    elif event.key == K_a:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # A
                            self.Ka[0] *= 1.2
                        else:  # a
                            self.Ka[0] /= 1.2
                    elif event.key == K_d:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:  # D
                            self.Kd[0] *= 1.2
                        else:  # d
                            self.Kd[0] /= 1.2
                    elif event.key == K_s:
                        if pygame.key.get_mods() & pygame.KMOD_SHIFT: # S
                            self.Ks[0] *= 1.2
                        else:  # s
                            self.Ks[0] /= 1.2
                    elif event.key == K_w:
                        self.flag_flying = not self.flag_flying


            self.Render()
            pygame.display.flip()

            dt = 0.1

            self.bird_angle += self.bird_speed*dt
            self.wing += 10.0*self.wing_speed*dt
            self.wing += 10.0*self.wing_speed*dt
            wing = self.wing - 2*np.pi*np.floor(self.wing/(2*np.pi))
            wing = 0.5*(np.pi/2-wing if wing < np.pi else wing-3*np.pi/2)
            self.left_wing, self.right_wing = wing, -wing

            if self.flag_flying:
                self.flag_time += dt
                self.a[2] = 0.3*np.sin(2*np.pi*self.flag_time/15.0)
                self.da[1] = 0.15*np.cos(2*np.pi*self.flag_time/19.0)
                self.b[2] = 0.2*np.sin(2*np.pi*self.flag_time/26.0)
                self.db[2] = 0.2*np.cos(2*np.pi*self.flag_time/37.0)

            self.time += dt

if __name__ == "__main__":
    c = Context()
    c.Run()