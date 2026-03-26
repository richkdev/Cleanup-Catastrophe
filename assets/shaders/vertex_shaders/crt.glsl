#version 300 es

layout (location = 0) in vec2 vert;
layout (location = 1) in vec2 in_text;
out vec2 vertex;

void main() {
    gl_Position = vec4(vert, 0.0, 1.0);
    vertex = in_text;
}