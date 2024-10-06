# /// script
# dependencies = [
#  "pygame-ce",
#  "zengl"
# ]
# ///

# based on:
#   https://github.com/szabolcsdombi/zengl/blob/main/examples/pygbag/main.py
#   https://github.com/pygame-web/showcases/blob/main/org/zengl/zengl-normal-mapping/zengl-normal-mapping.py
# run this command
# pygbag --PYBUILD 3.12 --ume_block 0 --template noctx.tmpl "tests\zengl_test\main.py"

import asyncio
import os
import sys
import pygame
import zengl

pygame.init()
pygame.display.set_mode((640, 480), flags=pygame.OPENGL, vsync=True)

# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
# pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)

ctx = zengl.context()

window_size = pygame.display.get_window_size()
image = ctx.image(window_size, 'rgba8unorm')
overlay = ctx.image(window_size, 'rgba8unorm')

vertexShader = """
#version 300 es

vec2 vertices[3] = vec2[](
    vec2(-1.0, -1.0),
    vec2(3.0, -1.0),
    vec2(-1.0, 3.0)
);

out lowp vec2 vertex;

void main() {
    gl_Position = vec4(vertices[gl_VertexID], 0.0, 1.0);
    vertex = vertices[gl_VertexID];
}
"""

fragmentShader = """
#version 300 es

uniform sampler2D Layer1;
uniform sampler2D Layer2;

in lowp vec2 vertex;

layout (location = 0) out vec4 out_color;

void main() {
    vec2 uv = vertex * 0.5 + 0.5;
    vec4 color1 = texture(Layer1, uv);
    vec4 color2 = texture(Layer2, uv);
    out_color = color1 * (1.0 - color2.a) + color2 * color2.a;
}
"""

pipeline = ctx.pipeline(
    vertex_shader=vertexShader,
    fragment_shader=fragmentShader,
    layout=[
        {
            'name': 'Layer1',
            'binding': 0,
        },
        {
            'name': 'Layer2',
            'binding': 1,
        },
    ],
    resources=[
        {
            'type': 'sampler',
            'binding': 0,
            'image': image,
        },
        {
            'type': 'sampler',
            'binding': 1,
            'image': overlay,
        },
    ],
    framebuffer=None,
    viewport=(0, 0, *window_size),
    topology='triangles',
    vertex_count=3,
)

rectangle = pygame.Surface((100, 200))
rectangle.fill(pygame.Color(255, 255, 255))

screen = pygame.surface.Surface(window_size).convert_alpha()
clock = pygame.Clock()
FPS = 100


async def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # mouse_x = mouse_x / size[0] - 0.5
        # mouse_y = 0.5 - mouse_y / size[1]

        ctx.new_frame()
        image.write(os.urandom(window_size[0] * window_size[1] * 4))

        screen.fill((0, 0, 0))
        screen.blit(rectangle, (10, 10))

        overlay.write(pygame.image.tobytes(screen, 'RGBA', flipped=True))
        pipeline.render()
        ctx.end_frame()

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(0)

asyncio.run(main())
