#version 300 es
precision highp float;

uniform sampler2D MainTexture;

in vec2 vertex;
layout (location = 0) out vec4 out_color;

void main() {
    vec2 uv = vertex * 0.5 + 0.5;
    vec4 color = texture(MainTexture, uv);
    out_color = color * color.a;
}