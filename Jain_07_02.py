#Jain, Kritika
#1001-093-381
#2017-12-06
#Assignment_07_02

shader_codes = {
    "std": (
        '''
        #version 330 core

        layout (location = 0) in vec3 position;
        layout (location = 1) in vec3 normal;

        uniform mat4 p = mat4(1.0);  // projection matrix
        uniform mat4 v = mat4(1.0);  // view matrix
        uniform mat4 m = mat4(1.0);  // model matrix

        uniform vec4 color;  // opject color
        uniform vec3 eye; // eye position

        out vec4 pos;
        out vec4 c;
        out vec3 n;
        out vec3 e;

        void main(){
            pos = m * vec4(position, 1.0);
            gl_Position = p * v * pos;
            c = color;
            n = normalize(normal);//(m * vec4(normal, 0.0)).xyz;
            e = normalize(eye - pos.xyz);
        }
        ''',
        '''
        #version 330 core

        in vec4 pos;
        in vec4 c;
        in vec3 n;
        in vec3 e;

        uniform vec3 light;
        uniform vec3 Ka;
        uniform float Ia;
        uniform vec3 Kd;
        uniform float Id;
        uniform vec3 Ks;
        uniform float Is;

        layout (location = 0) out vec4 col;

        void main(){
        vec3 sun = light;
            //col = vec4(c.xyz*(0.5 + 0.6*dot(n, sun)
            //        + 0.6*clamp(dot(e, reflect(-sun, n)), 0, 1)), c.a);
            vec3 ray = normalize(pos.xyz - light);
            vec3 a = Ka*Ia; // ambient
            vec3 d = Kd*dot(ray, n)*Id;
            vec3 s = Ks*dot(e, reflect(ray, n))*Is;
            vec3 I = a+d+s;
            col = vec4(I*c.rgb, c.a);
        }
        '''
    )
}

from OpenGL.GL.shaders import *
from OpenGL.GL import *

class Shaders:

    std = None
    std_uniforms = {}

    def __init__(self):
        vs = compileShader(shader_codes["std"][0], GL_VERTEX_SHADER)
        fs = compileShader(shader_codes["std"][1], GL_FRAGMENT_SHADER)
        self.std = compileProgram(vs, fs)
        for name in ["p", "v", "m", "color", "eye", "pos", "light", "Ka", "Ia", "Kd", "Id", "Ks", "Is"]:
            self.std_uniforms[name] = glGetUniformLocation(self.std, name)